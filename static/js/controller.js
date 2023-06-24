import {Game} from './game.js';
import {View} from './view.js';
class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.player = -1;
        this.run()
        this.thinking = false
        this.isWin = false;
    }

    refresh(history){
        this.player = -1
        this.model = new Game(3,3)
        for(const index of history){
            this.model.play(index,this.player)
            this.player *=-1
        }
        this.view.refresh(history)
    }
    updateWin() {
        let [win,numGrid] = this.model.lastGridWin()
        if (win !== 0) this.view.markGrid(numGrid,win)
        const winner = this.model.evaluate()

        if (winner !== 0){
            this.isWin = true
            this.view.DisplayWin(winner)
        }
        return winner

    }
    run() {
        const check = document.getElementById("displayValuation")
        const buttonReport = document.getElementById("report")
        check.onchange = () => {
            this.view.displayValuation(check.checked)
        }
        buttonReport.onclick = () => {
                let observation = prompt("Give us your observation about this bad move :")
                fetch('http://127.0.0.1:5000/save_history', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({history:this.model.history,"observation":observation}),
                })
        }



        for (let i = 0; i < 9; i++) {
            this.view.createBoard(i);
        }

        for (let i = 0; i < this.view.boardElements.length; i++) {
            let button = this.view.boardElements[i];
            button.onclick = () => {
                if (this.thinking || this.isWin) return
                let index_play = Number(button.id);
                this.model.play(index_play,this.player)
                this.view.markButton(button,this.player)
                this.player *= -1


                this.view.updateButtonDisabled(this.model.validActions())
                let win = this.updateWin()
                if(win) return



                // get IA move
                this.thinking = true
                this.view.thinking(this.thinking)
                fetch('http://127.0.0.1:5000/best_move', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({last_play:this.model.lastPlay}),
                })
                .then(response => {
                    console.log(response)
                    return response.json()
                })
                .then(data => {
                    let bestMove = data['best_move'];
                    let valuations = data['valuations'];

                    this.model.play(bestMove,this.player)
                    console.log("play: "+bestMove)

                    let button = document.getElementById(bestMove)
                    this.view.markButton(button,this.player)
                    this.player *= -1
                    view.setValuation(valuations)

                    this.thinking = false
                    this.view.thinking(this.thinking)
                    this.updateWin()
                    this.view.updateButtonDisabled(this.model.validActions())

                });





            }
        }
    }

}

// Initialisation
let model = new Game(3,3);
let view = new View();

document.controller = new Controller(model, view);
