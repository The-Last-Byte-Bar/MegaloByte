import os
import json
from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import Address, ErgoValue
import logging
import datetime
import sys
from java.lang import Long
import hashlib
from nft_register_helper import create_nft_registers

# Constants
ERG_TO_NANOERG = 1e9
MIN_BOX_VALUE = int(0.005 * ERG_TO_NANOERG)  # 0.005 ERG for NFT box
FEE = int(0.001 * ERG_TO_NANOERG)  # 0.001 ERG fee

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/nft_minting_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def load_config(config_path: str = 'config.json') -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Required configuration fields
        required_fields = {
            'node': ['url', 'apiKey', 'network'],
            'explorer': ['url'],
            'wallet': ['address'],
            'nft': [
                'name', 'description', 'decimals', 'edition', 
                'event', 'date', 'creator', 'project',
                'collectionName', 'collectionFamily'
            ],
            'ipfs': ['hash', 'filename']
        }

        # Validate configuration
        for section, fields in required_fields.items():
            if section not in config:
                raise ValueError(f"Missing section in config: {section}")
            for field in fields:
                if field not in config[section]:
                    raise ValueError(f"Missing field in {section}: {field}")

        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {str(e)}")

logger = setup_logging()

def calculate_image_hash(filepath: str) -> bytes:
    """Calculate SHA256 hash of image file"""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).digest()

def log_config(config: dict):
    """Log configuration settings"""
    logger.info("Starting NFT minting process with configuration:")
    logger.info(f"Network Type: {config['node']['network']}")
    logger.info(f"Explorer URL: {config['explorer']['url']}")
    logger.info(f"Sender Address: {config['wallet']['address']}")
    logger.info(f"NFT Name: {config['nft']['name']}")
    logger.info(f"NFT Description: {config['nft']['description']}")
    logger.info(f"NFT Edition: {config['nft']['edition']}")
    logger.info(f"Collection Name: {config['nft']['collectionName']}")
    logger.info(f"Collection Family: {config['nft']['collectionFamily']}")
    logger.info(f"IPFS URL: ipfs://{config['ipfs']['hash']}/{config['ipfs']['filename']}")
    logger.info(f"Minimum Box Value: {MIN_BOX_VALUE/ERG_TO_NANOERG:.9f} ERG")

def create_detailed_description(config: dict) -> str:
    """Create a detailed description combining multiple metadata fields"""
    nft_config = config['nft']
    return (f"{nft_config['description']}\n\n"
            f"Edition: {nft_config['edition']}\n"
            f"Event: {nft_config['event']}\n"
            f"Date: {nft_config['date']}\n"
            f"Creator: {nft_config['creator']}\n"
            f"Project: {nft_config['project']}\n"
            f"Collection: {nft_config['collectionName']}\n"
            f"Family: {nft_config['collectionFamily']}")

def mint_nft(config_path: str = 'config.json'):
    """Main function to mint NFT"""
    try:
        # Load configuration
        config = load_config(config_path)
        
        # Log configuration
        log_config(config)
        
        # Initialize ErgoAppKit
        logger.info("Initializing ErgoAppKit...")
        ergo = ErgoAppKit(
            config['node']['url'],
            config['node']['network'],
            config['explorer']['url'],
            config['node']['apiKey']
        )
        logger.info("ErgoAppKit initialized successfully")

        # Calculate total ERG needed
        total_erg_needed = MIN_BOX_VALUE + FEE
        logger.info(f"Total ERG needed: {total_erg_needed/ERG_TO_NANOERG:.9f} ERG")

        # Get unspent boxes
        unspent_boxes = ergo.boxesToSpend(config['wallet']['address'], total_erg_needed)
        token_id = unspent_boxes[0].getId().toString()
        logger.info(f"Token ID will be: {token_id}")

        # Calculate image hash from local file
        image_hash = calculate_image_hash('asset.svg')
        logger.info("Calculated image hash successfully")
        
        # Construct IPFS URL
        ipfs_url = f"ipfs://{config['ipfs']['hash']}/{config['ipfs']['filename']}"
        logger.info(f"Using IPFS URL: {ipfs_url}")

        # Create detailed description
        detailed_description = create_detailed_description(config)

        # Create registers using helper function
        logger.info("Creating NFT registers...")
        registers = create_nft_registers(
            ergo=ergo,
            name=config['nft']['name'],
            description=detailed_description,
            decimals=config['nft']['decimals'],
            nft_type=1,
            image_hash=image_hash,
            ipfs_url=ipfs_url
        )
        logger.info("NFT registers created successfully")

        # Create NFT output box
        nft_output_box = ergo.buildOutBox(
            value=MIN_BOX_VALUE,
            tokens={token_id: 1},
            registers=registers,
            contract=ergo.contractFromAddress(config['wallet']['address'])
        )

        # Build and sign transaction
        logger.info("Building unsigned transaction...")
        unsigned_tx = ergo.buildUnsignedTransaction(
            inputs=unspent_boxes,
            outputs=[nft_output_box],
            fee=FEE,
            sendChangeTo=Address.create(config['wallet']['address']).getErgoAddress()
        )
        
        logger.info("Signing transaction with node wallet...")
        signed_tx = ergo.signTransactionWithNode(unsigned_tx)
        logger.info("Submitting transaction to network...")
        tx_id = ergo.sendTransaction(signed_tx)
        
        logger.info("NFT minted successfully!")
        logger.info(f"Transaction ID: {tx_id}")
        logger.info(f"Token ID: {token_id}")
        
        # Log explorer links
        explorer_base = config['explorer']['url'].replace('/api/v1', '')
        logger.info(f"Transaction explorer link: {explorer_base}/transactions/{tx_id}")
        logger.info(f"Token explorer link: {explorer_base}/tokens/{token_id}")
        
        return tx_id, token_id

    except Exception as e:
        logger.error(f"Error minting NFT: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        # Allow config file path to be specified as command line argument
        config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
        mint_nft(config_path)
    except Exception as e:
        logger.error("NFT minting process failed", exc_info=True)
        sys.exit(1)