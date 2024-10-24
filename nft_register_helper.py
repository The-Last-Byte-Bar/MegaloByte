from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import ErgoValue
from typing import List
from java.lang import Long as JLong
import jpype

def create_nft_registers(
    ergo: ErgoAppKit,
    name: str,
    description: str,
    decimals: int,
    nft_type: int,
    image_hash: bytes,
    ipfs_url: str
) -> List[ErgoValue]:
    """
    Create properly typed registers for NFT minting using JPype byte arrays
    """
    # Convert to JPype byte arrays
    name_bytes = jpype.JArray(jpype.JByte)(bytes(name.encode()))
    description_bytes = jpype.JArray(jpype.JByte)(bytes(description.encode()))
    ipfs_bytes = jpype.JArray(jpype.JByte)(bytes(ipfs_url.encode()))
    image_hash_bytes = jpype.JArray(jpype.JByte)(image_hash)
    
    # Create registers using proper Java byte arrays
    registers = [
        # R4: Name as CollByte
        ErgoValue.of(name_bytes),
        
        # R5: Description as CollByte  
        ErgoValue.of(description_bytes),
        
        # R6: Decimals as Long
        ErgoValue.of(JLong(decimals)),
        
        # R7: NFT Type as Long
        ErgoValue.of(JLong(nft_type)),
        
        # R8: Image Hash as CollByte
        ErgoValue.of(image_hash_bytes),
        
        # R9: IPFS URL as CollByte
        ErgoValue.of(ipfs_bytes)
    ]
    
    return registers