const SHA256 = require('crypto-js/sha256');

//Creation of the block
class Block{
    constructor(index, timestamp, transactions, previousHash = ''){
        this.timestamp = timestamp;
        this.transactions = transactions;
        this.previousHash = previousHash;
        this.hash = this.calculateHash();
        this.nonce = '0';
    }

    //Calculating the hash
    calculateHash(){
        return SHA256(this.index + this.previousHash + this.timestamp + JSON.stringify(this.data)+this.nonce).toString();

    }

    //Proof of work

    mineBlock(difficulty){
        while(this.hash.substring(0, difficulty) !== Array(difficulty + 1).join("0")){
            this.nonce++;                     //Prevents the hash of the blocks becoming the same if the content is the same
            this.hash = this.calculateHash(); //Hashing every block
        }
        console.log("Block mined: " + this.hash);
    }
}


class Blockchain{
        constructor(){
            this.chain = [this.createGenesisBlock()];
            this.difficulty = 4;
        }
        //The first block should be created manually
        createGenesisBlock(){
            return new Block("01/03/2021", "Genesis block", "0");
        }

        getLatestBlock(){
            return this.chain[this.chain.length - 1];
        }

        //Responsible for adding a new block to the chain
        addBlock(newBlock){
            newBlock.previousHash = this.getLatestBlock().hash;
            newBlock.mineBlock(this.difficulty);
            this.chain.push(newBlock);
        }
        //Integrity check
        isChainValid(){
            for(let i = 1; i < this.chain.length; i++){
                const currentBlock = this.chain[i];
                const previousBlock = this .chain[i - 1];

                if(currentBlock.hash != currentBlock.calculateHash()){
                    return false;
                }

                if(currentBlock.previousHash != previousBlock.hash){
                    return false;
                }
            }
            return true;
        }
}
    

    let umicoin = new Blockchain();

    console.log('Mining block 1...');
    umicoin.addBlock(new Block(1, "10/04/2021",{amount: 4}));
    console.log('Mining block 2...');
    umicoin.addBlock(new Block(2, "12/04/2021",{amount: 10}));
    console.log('Mining block 3...');
    umicoin.addBlock(new Block(2, "12/04/2021",{amount: 1056}));
    console.log('Mining block 4...');
    umicoin.addBlock(new Block(2, "12/04/2021",{amount: 108}));
    console.log('Mining block 5...');
    umicoin.addBlock(new Block(2, "12/04/2021",{amount: 107}));

    console.log('Is Blockchain Valid? ' + umicoin.isChainValid());

    umicoin.chain[1].data = {amount : 100};
    //umicoin.chain[1].hash = umicoin.chain[1].calculateHash();
    console.log('Is Blockchain Valid? ' + umicoin.isChainValid());
     
   //console.log(JSON.stringify(umicoin, null, 4));
