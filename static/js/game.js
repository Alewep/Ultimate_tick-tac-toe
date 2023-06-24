export class Game {
    constructor(blockSize, nBlock) {
        this.blockSize = blockSize;
        this.nBlock = nBlock;
        this.blockSizeSquared = blockSize * blockSize;
        this.nBlockSquared = nBlock * nBlock;
        this.board = new Array(this.blockSizeSquared * this.nBlockSquared).fill(0);
        this.bigBoard = new Array(this.nBlockSquared).fill(0);
        this.gridToUpdate = new Set();
        this.lastPlay = -1;
        this.turn = 0;
    }

    coordinateToIndex(row, col) {
        let gridRow = Math.floor(row / this.blockSize);
        let gridCol = Math.floor(col / this.blockSize);
        let gridNum = gridRow * this.nBlock + gridCol;

        let localRow = row % this.blockSize;
        let localCol = col % this.blockSize;

        return gridNum * this.blockSizeSquared + (localRow * this.blockSize + localCol);
    }

    updateBigBoard() {
        for (let gridNum of this.gridToUpdate) {
            if (this.bigBoard[gridNum] !== 0) continue;

            let localBoard =  this.board.slice(gridNum * this.blockSizeSquared, (gridNum + 1) * this.blockSizeSquared)
            this.bigBoard[gridNum] = checkWin(localBoard);

        }

        this.gridToUpdate.clear();
    }

    play(index, player = 1) {
        if (this.board[index] !== 0) {
            throw new Error('Cell already occupied');
        }
        if (player !== 1 && player !== -1) {
            throw new Error('The player id is not correct');
        }

        this.board[index] = player;
        this.lastPlay = index;
        this.gridToUpdate.add(Math.floor(index / this.blockSizeSquared));
        this.turn++;
    }

    indexToCoordinate(index) {
        let gridNum = Math.floor(index / this.blockSizeSquared);

        let localIndex = index % this.blockSizeSquared;

        let gridRow = Math.floor(gridNum / this.nBlock);
        let gridCol = gridNum % this.nBlock;

        let localRow = Math.floor(localIndex / this.blockSize);
        let localCol = localIndex % this.blockSize;

        let row = gridRow * this.blockSize + localRow;
        let col = gridCol * this.blockSize + localCol;

        return {row, col};
    }

    evaluate() {
        let winner = checkWin(this.bigBoard);
        if (winner !== null) {
            return winner;
        }

        if (this.turn === this.blockSizeSquared * this.nBlockSquared) {
            return  this.bigBoard.reduce((total, value) => total + value, 0); // The game is a draw
        }

        return null; // The game is not over
    }

    validActions() {
        let validActions = [];
        let gridNum = this.lastPlay % this.blockSizeSquared;

        this.updateBigBoard();

        if (this.lastPlay >= 0 && this.bigBoard[gridNum] === 0) {
            for (let i = gridNum * this.blockSizeSquared; i < (gridNum + 1) * this.blockSizeSquared; i++) {
                if (this.board[i] === 0) {
                    validActions.push(i);
                }
            }
        } else {
            for (let i = 0; i < this.board.length; i++) {
                if (this.board[i] === 0 && this.bigBoard[Math.floor(i / this.blockSizeSquared)] === 0) {
                    validActions.push(i);
                }
            }
        }

        return validActions;
    }

    lastGridWin(){
        this.updateBigBoard()
        const numGrid = Math.floor(this.lastPlay / this.blockSizeSquared)
        const win = this.bigBoard[numGrid]
        return [win,numGrid]
    }

}

const winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

function checkWin(board) {
    let count = 0
    for (let i=0;i<board.length;++i){
        count += Math.abs(board[i])
    }
    for (let i = 0; i < winning_combinations.length; i++) {

        const [a, b, c] = winning_combinations[i];
        if (Boolean(board[a]) && board[a] === board[b] && board[a] === board[c]) {
            return board[a];
        }
    }
    if (count === 9) return null;
    else return 0
}