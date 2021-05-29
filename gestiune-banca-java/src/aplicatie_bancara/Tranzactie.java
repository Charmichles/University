package aplicatie_bancara;

import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.io.FileWriter;
import java.io.IOException;
import java.text.ParseException;

public class Tranzactie {
    public static FileWriter writer;
    public static Integer nr_tranzactii;
    private final String id;
    private final String expeditor, destinatar;
    private final String valuta;
    private final Float valoare, soldul_zilei;
    private final String mesaj;
    private Date data;

    static {
        nr_tranzactii = 0;
        try {
            writer = new FileWriter("csv_db\\tranzactii.csv");
            writer.write("id,id_expeditor,id_destinatar,valuta,valoare,soldul_zilei,mesaj,data\n");
        }
        catch (IOException e) {
            System.out.print("Error occured while creating FileWriter for Tranzactie\n");
            e.printStackTrace();
        }
    }

    public static Tranzactie fromString(String s) {
        String split[] = s.split(",");
        return new Tranzactie(split[0], split[1], split[2], split[3], split[4], split[5], split[6], split[7]);
    }

    public Tranzactie(ContCurent expeditor, ContCurent destinatar, String valuta, Float valoare, String mesaj, Float soldul_zilei) {
        nr_tranzactii++;
        this.id = nr_tranzactii.toString();
        this.expeditor = expeditor.getId();
        this.destinatar = destinatar.getId();
        this.valuta = valuta;
        this.valoare = valoare;
        this.soldul_zilei = soldul_zilei;
        this.mesaj = mesaj;
        this.data = new Date();
    }

    public Tranzactie(String id, String expeditor, String destinatar, String valuta, String valoare, String soldul_zilei, String mesaj, String data)
    {
        this.id = id;
        this.expeditor = expeditor;
        this.destinatar = destinatar;
        this.valuta = valuta;
        this.valoare = Float.parseFloat(valoare);
        this.soldul_zilei = Float.parseFloat(soldul_zilei);
        this.mesaj = mesaj;
        DateFormat format = new SimpleDateFormat("E MMMM d kk:mm:ss zzzz yyyy");
        try {
            this.data = format.parse(data);
        }
        catch (ParseException e) {
            System.out.print("Error occured while parsing date from csv.\n");
            e.printStackTrace();
        }
    }

    public String getId() {
        return id;
    }

    public String getExpeditor() {
        return expeditor;
    }

    public String getDestinatar() {
        return destinatar;
    }

    public String getValuta() {
        return valuta;
    }

    public Float getValoare() {
        return valoare;
    }

    public String getMesaj() {
        return mesaj;
    }

    public Date getData() {
        return data;
    }

    public Float getSoldulZilei() {
        return soldul_zilei;
    }

    public void efectueazaTranzactie(ContCurent expeditor, ContCurent destinatar) {
        if (expeditor == destinatar) {
            return;
        }
        if (expeditor.retrageFonduri(valoare, valuta) != -1) {
            destinatar.adaugaFonduri(valoare, valuta);
            expeditor.addTranzactie(this);
            destinatar.addTranzactie(this);
        }
    }

    public void writeToFile() {
        try {
            writer.write(id + ',' + expeditor + ',' + destinatar + ',' + valuta + ',' + valoare + ',' + soldul_zilei + ',' + mesaj + ',' + data + '\n');
        }
        catch (IOException e) {
            System.out.print("Error occured while writing to file csv_db/tranzactii.csv.\n");
            e.printStackTrace();
        }
    }

    @Override
    public String toString() {
        return "Tranzactie{" +
            "expeditor='" + expeditor + "'" +
            ", destinatar='" + destinatar + "'" +
            ", valuta='" + valuta + "'" +
            ", valoare='" + valoare + "'" +
            ", soldul zilei='" + soldul_zilei + "'" +
            ", mesaj='" + mesaj + "'" +
            ", data='" + data + "'" +
            "}";
    }
}
