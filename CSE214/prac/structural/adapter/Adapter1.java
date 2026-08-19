
public class Adapter1 {
    public static void main(String[] args) {
        MediaPlayer player = new MediaAdapter();

        player.play("movie.mp4");
        player.play("rec.avc");
    }
}

interface MediaPlayer {
    void play(String filename);
}

class AdvancedPlayer {
    public void playAVC(String file) {
        System.out.println("AVC: " + file);
    }

    public void playMP4(String file) {
        System.out.println("MP4: " + file);
    }
}

class MediaAdapter implements MediaPlayer {
    private AdvancedPlayer adaptee;

    public MediaAdapter() {
        this.adaptee = new  AdvancedPlayer();
    }

    @Override
    public void play(String filename) {
        if (filename.endsWith(".avc")) adaptee.playAVC(filename);
        else if (filename.endsWith(".mp4")) adaptee.playMP4(filename);
    }
}