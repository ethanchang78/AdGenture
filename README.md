## AdGenture

A simple UI using the python tkinter library. This allows the user to click a button to choose their seed text to start the story. The application displays the image, text, and options for the current time step. Choosing an option clears the screen and displays the next events. We limit play to five rounds before forcing a concussion. 

You can run the UI after cloning the GitHub repository like so:
```
python app.py
```

For model weights, you can access them here:
https://drive.google.com/drive/folders/1oTVD4C_WoJrBuP23Y0F6lhIIdpZSkObc?usp=sharing

GitHub Repositories we used/built upon:
* Used: Make Your Own Sprites: Aliasing-Aware and Cell-Controllable Pixelization (https://github.com/WuZongWei6/Pixelization) 
* Built Upon: Wuerstchen (https://github.com/dome272/Wuerstchen)
    * Modified Stage C Training Loop from using DDP to using Single GPU, also added Custom Dataset
    * Used given Inference Script

