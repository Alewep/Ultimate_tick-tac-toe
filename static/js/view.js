export class View {
    constructor() {
        this.boardElements = [];
    }

    createBoard(i) {
        let board = document.getElementById("board"+i);
        for (let x = 0; x < 3; x++) {
            let row = document.createElement('tr');
            for (let y = 0; y < 3; y++) {
                let cell = document.createElement('td');
                let button = document.createElement('button');
                button.id = ((x*3+y) + i*9).toString();
                button.innerHTML = '&nbsp;';
                cell.appendChild(button);
                row.appendChild(cell);
                this.boardElements.push(button);
            }
            board.appendChild(row);
        }
    }

    markButton(button, symbol) {
        button.style.backgroundColor = (symbol === 1) ? 'Tomato':'DodgerBlue';
        button.innerHTML = (symbol === 1) ? 'X':'O';
        button.disabled = true;
    }

    markGrid(id,symbol){
        const grid = document.getElementById("board"+id)
        grid.innerHTML = '';
        let winnerCell = document.createElement('td');
        winnerCell.innerHTML = (symbol === 1) ? 'X':'O';
        winnerCell.className = "winCell";
        winnerCell.style.backgroundColor = (symbol === 1) ? 'Tomato':'DodgerBlue';
        let winnerRow = document.createElement('tr');
        winnerRow.appendChild(winnerCell);
        grid.appendChild(winnerRow);
    }

    updateButtonDisabled(indexsToEnable) {
        for (let i = 0; i < this.boardElements.length; i++) {
            const enable = indexsToEnable.includes(Number(this.boardElements[i].id))
            this.boardElements[i].disabled = !enable;
        }
    }

    DisplayWin(winner) {
        const body = document.getElementsByTagName("body")[0]
        let winMsg = document.createElement('p');
        let msg = (winner === 1) ? "I have win the game, you're suck human 🥱":"You won, but I'm still superior 😈"
        winMsg.innerHTML = msg
        winMsg.className = "winMsg"
        body.appendChild(winMsg)
    }

    thinking(state){
        const msg = document.getElementById("status")
        msg.hidden = !state
    }

    setValuation(valuation){
        const buttons = document.querySelectorAll('.game button');
        const check = document.getElementById("displayValuation")
        buttons.forEach((button, index) => {
            index = Number(button.id)
            button = button.parentNode

            const existingValuationElement = button.querySelector('.valuation');
            if (existingValuationElement !== null) existingValuationElement.remove()
            if (valuation.hasOwnProperty(index)) {
              const valuationElement = document.createElement('span');
              valuationElement.className = 'valuation';
              valuationElement.hidden = !check.checked
              valuationElement.innerHTML = valuation[index].toFixed(2);;
              button.appendChild(valuationElement);
            }
        });
    }

    displayValuation(isDisplay){
        const valuations = document.querySelectorAll('.valuation');
        valuations.forEach((valuation) =>{
            valuation.hidden = !isDisplay
        });

    }


}

