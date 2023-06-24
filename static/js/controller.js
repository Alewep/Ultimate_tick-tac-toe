import {Game} from './game.js';
import {View} from './view.js';
class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.player = -1;
        this.run()
        this.thinking = false
    }
    updateWin() {
        let [win,numGrid] = this.model.lastGridWin()
        if (win !== 0) this.view.markGrid(numGrid,win)
        const winner = this.model.evaluate()
        if (winner !== 0){
            this.view.DisplayWin(winner)
        }
    }
    run() {
        for (let i = 0; i < 9; i++) {
            this.view.createBoard(i);
        }

        for (let i = 0; i < this.view.boardElements.length; i++) {
            let button = this.view.boardElements[i];
            button.onclick = () => {
                if (this.thinking) return
                let index_play = Number(button.id);
                this.model.play(index_play,this.player)
                this.view.markButton(button,this.player)
                this.player *= -1


                this.view.updateButtonDisabled(this.model.validActions())
                this.updateWin()

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
                    this.model.play(bestMove,this.player)
                    console.log("play: "+bestMove)

                    let button = document.getElementById(bestMove)
                    this.view.markButton(button,this.player)
                    this.player *= -1

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
