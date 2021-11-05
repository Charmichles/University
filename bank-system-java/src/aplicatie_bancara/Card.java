package aplicatie_bancara;

import java.util.Date;
import java.text.ParseException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.io.FileWriter;
import java.io.IOException;

public class Card {
    public static FileWriter writer;
    private final String numar, nume;
    private Integer PIN;
    private Date data_expirare;
    private final Integer CVV;

    static {
        try {
            writer = new FileWriter("csv_db\\carduri.csv");
            writer.write("numar,nume,PIN,data_expirare,CVV\n");
        }
        catch (IOException e) {
            System.out.print("Error occured while creating FileWriter for Card\n");
            e.printStackTrace();
        }
    }

    public static Card fromString(String s) {
        String split[] = s.split(",");
        return new Card(split[0], split[1], split[2], split[3], split[4]);
    }

    public Card(String numar, Date data_expirare, Integer CVV, String nume, Integer PIN) {
        this.numar = numar;
        this.data_expirare = data_expirare;
        this.CVV = CVV;
        this.nume = nume;
        this.PIN = PIN;
    }

    public Card(String numar, String nume, String PIN, String data_expirare, String CVV) {
        this.numar = numar;
        this.nume = nume;
        this.PIN = Integer.parseInt(PIN);
        DateFormat format = new SimpleDateFormat("E MMMM d kk:mm:ss zzzz yyyy");
        try {
            this.data_expirare = format.parse(data_expirare);
        }
        catch (ParseException e) {
            System.out.print("Error occured while parsing date from csv.\n");
            e.printStackTrace();
        }
        this.CVV = Integer.parseInt(CVV);
    }

    public String getNumar() {
        return numar;
    }

    public Date getData_expirare() {
        return data_expirare;
    }

    public Integer getCVV() {
        return CVV;
    }

    public String getNume() {
        return nume;
    }

    public Integer getPIN() {
        return PIN;
    }

    public void setPIN(Integer PIN) {
        this.PIN = PIN;
    }

    public void writeToFile() {
        try {
            writer.write(numar + ',' + nume + ',' + PIN + ',' + data_expirare + ',' + CVV + '\n');
        }
        catch (IOException e) {
            System.out.print("Error occured while writing to file csv_db/carduri.csv.\n");
            e.printStackTrace();
        }
    }

    @Override
    public String toString() {
        return "Card{" +
            "numar='" + numar + "'" +
            ", nume='" + nume + "'" +
            ", PIN='" + PIN + "'" +
            ", data_expirare='" + data_expirare + "'" +
            ", CVV='" + CVV + "'" +
            "}";
    }
}
