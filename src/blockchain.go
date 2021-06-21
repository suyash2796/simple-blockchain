package main
import(
	"bytes"
	"crypto/sha256"
	"fmt"
)

type Block struct{
	Hash []byte
	Data []byte
	PrevHash []byte
}

type BlockChain struct{
	chain []*Block
}

func(b *Block) ProofofWork(){
	code := bytes.Join([][]byte{b.Data, b.PrevHash},[]byte{})
	hash := sha256.Sum256(code)
	b.Hash =hash[:]
}

func createBlock(data string, prevHash []byte) *Block{
	block := &Block{[]byte{}, []byte(data),prevHash}
	block.ProofofWork()
	return block
}

func (chain *BlockChain) AddBlock(data string){
	prev :=chain.chain[len(chain.chain)-1]
	new := createBlock(data, prev.Hash)
	chain.chain = append(chain.chain, new)
}

func Genesis() * Block{
	return createBlock("Genesis", []byte{})
}

func InitBlockChain() *BlockChain{
	return &BlockChain{[] *Block{Genesis()}}
}

func main(){
	chain:=InitBlockChain()
	chain.AddBlock("first block after genesis")
	chain.AddBlock("second block")
	 for _,block := range chain.chain{
		 fmt.Printf("Previous : %x\n", block.PrevHash)
		 fmt.Printf("Data : %x\n", block.Data)
		 fmt.Printf("Hash : %x\n", block.Hash)
	 }
}