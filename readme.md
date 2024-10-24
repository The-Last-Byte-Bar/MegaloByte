# 🦈 Megalobyte

Megalobyte is a streamlined Python tool for minting NFTs on the Ergo blockchain. Named after the legendary Megalodon, this tool aims to be the apex predator of NFT minting solutions - powerful, efficient, and reliable.

## 🌟 Features

- Single-transaction NFT minting on Ergo blockchain
- Comprehensive metadata support
- IPFS integration
- Automatic image hash generation
- Detailed transaction logging
- JSON-based configuration
- Supports both mainnet and testnet

## 🛠 Prerequisites

- Python 3.8+
- Java 8 or newer
- Access to an Ergo node
- Node API key
- Sufficient ERG for minting (minimum 0.006 ERG per NFT)

## ⚡ Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/megalobyte.git
cd megalobyte
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create your configuration file (`config.json`):
```json
{
    "node": {
        "url": "http://your.node.url:9053",
        "apiKey": "your_api_key",
        "network": "mainnet"
    },
    "explorer": {
        "url": "https://api.ergoplatform.com/api/v1"
    },
    "wallet": {
        "address": "your_wallet_address"
    },
    "nft": {
        "name": "Your NFT Name",
        "description": "Your NFT Description",
        "decimals": 0,
        "edition": "Edition #1",
        "event": "Event Name",
        "date": "2024-10-24",
        "creator": "Creator Name",
        "project": "Project Name",
        "collectionName": "Collection Name",
        "collectionFamily": "Collection Family"
    },
    "ipfs": {
        "hash": "your_ipfs_hash",
        "filename": "your_filename"
    }
}
```

4. Place your NFT image as `asset.svg` in the project root

5. Run the minting script:
```bash
python mint_nft.py
```

## 📁 Project Structure

```
megalobyte/
├── mint_nft.py            # Main minting script
├── nft_register_helper.py # Helper for NFT register creation
├── config.json           # Configuration file
├── asset.svg            # Your NFT image file
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── logs/               # Generated log files
```

## 💎 NFT Metadata

The tool supports comprehensive NFT metadata including:
- Name
- Description
- Edition number
- Event details
- Creation date
- Creator information
- Project details
- Collection information
- IPFS location
- Image hash

## 📝 Configuration

The `config.json` file contains all necessary settings:

- **node**: Your Ergo node connection details
  - `url`: Node URL
  - `apiKey`: Node API key
  - `network`: "mainnet" or "testnet"
  
- **explorer**: Ergo explorer settings
  - `url`: Explorer API URL

- **wallet**: Wallet settings
  - `address`: Your Ergo wallet address

- **nft**: NFT metadata
  - All relevant NFT information

- **ipfs**: IPFS settings
  - `hash`: IPFS hash of your NFT
  - `filename`: Filename in IPFS

## 📊 Logging

Logs are automatically generated in the `logs` directory with timestamp-based filenames. They include:
- Configuration details
- Transaction progress
- Success/failure information
- Explorer links
- Token IDs and transaction IDs

## 🔧 Technical Details

- Minimum box value: 0.005 ERG
- Transaction fee: 0.001 ERG
- Total cost per mint: 0.006 ERG
- Supports SVG image format
- Generates SHA256 image hash
- Uses ErgoAppKit for blockchain interaction

## 🚧 Error Handling

The tool includes comprehensive error handling for:
- Configuration issues
- Network problems
- Insufficient funds
- Transaction failures
- Invalid metadata

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Support

For issues, questions, or contributions:
1. Create an issue in the GitHub repository
2. Submit a pull request with fixes or improvements
3. Contact the maintainers

## ⚠️ Disclaimer

This tool is provided as-is. Please ensure you have basic understanding of Ergo blockchain and NFT minting before use. Always test on testnet first.

---

🦈 Megalobyte is not affiliated with the Ergo Platform. It is a community-built tool for the Ergo ecosystem.