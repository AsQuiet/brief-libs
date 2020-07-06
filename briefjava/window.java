package briefjava;

import javax.swing.JFrame;

public class window {

    // basic swing components
    JFrame frame;

    // frame settings
    int width, height;
    String title;
    String iconPath;

    public window() {
        title = "some window";
        width = 600;
        height = 400;

        frame = new JFrame(title);
        frame.setSize(width, height);
        frame.setResizable(false);
        frame.pack();
        frame.setVisible(true);
    }
    
}