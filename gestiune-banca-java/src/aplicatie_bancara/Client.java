package aplicatie_bancara;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
import java.io.FileWriter;
import java.io.IOException;

public class Client {
    public static FileWriter writer;
    private String nume, CNP, adresa, telefon;

    static {
        try {
            writer = new FileWriter("csv_db\\clienti.csv");
            writer.write("nume,CNP,adresa,telefon\n");
        }
        catch (IOException e) {
            System.out.print("Error occured while creating FileWriter for Client.\n");
            e.printStackTrace();
        }
    }

    public static Client fromString(String s) {
        String split[] = s.split(",");
        return new Client(split[0], split[1], split[2], split[3]);
    }

    public Client(String nume, String CNP, String adresa, String telefon) {
        this.nume = nume;
        this.CNP = CNP;
        this.adresa = adresa;
        this.telefon = telefon;
    }

    public String getNume() {
        return nume;
    }

    public void setNume(String nume) {
        this.nume = nume;
    }

    public String getCNP() {
        return CNP;
    }

    public void setCNP(String CNP) {
        this.CNP = CNP;
    }

    public String getAdresa() {
        return adresa;
    }

    public void setAdresa(String adresa) {
        this.adresa = adresa;
    }

    public String getTelefon() {
        return telefon;
    }

    public void setTelefon(String telefon) {
        this.telefon = telefon;
    }

    public static Client citesteClient(Scanner keyboard) {
        ArrayList<String> cereri, valori;
        cereri = new ArrayList<>(Arrays.asList("Nume", "CNP", "Adresa", "Telefon"));
        valori = new ArrayList<>();
        for (String cerere : cereri) {
            System.out.print(cerere + " client:\n");
            valori.add(keyboard.nextLine());
            System.out.print('\n');
        }
        return new Client(valori.get(0), valori.get(1), valori.get(2), valori.get(3));
    }

    public void writeToFile() {
        try {
            writer.write(nume + ',' + CNP + ',' + adresa + ',' + telefon + '\n');
        }
        catch (IOException e) {
            System.out.print("Error occured while writing to file csv_db/clienti.csv.\n");
            e.printStackTrace();
        }
    }

    public boolean equals(Client c) {
        return CNP.equals(c.getCNP());
    }

    @Override
    public String toString() {
        return "Client{" +
                "nume='" + nume + '\'' +
                ", CNP='" + CNP + '\'' +
                ", adresa='" + adresa + '\'' +
                ", telefon='" + telefon + '\'' +
                '}';
    }
}
