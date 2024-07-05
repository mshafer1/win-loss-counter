import win_loss_counter


if __name__ == "__main__":
    win_loss_counter.socketio.run(win_loss_counter.app, host="0.0.0.0", debug=win_loss_counter._DEBUG)
