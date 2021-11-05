package aplicatie_bancara;

import java.util.Date;
import java.io.FileWriter;
import java.io.IOException;
import java.text.ParseException;
import java.util.HashMap;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

public class ContDepozit extends Cont{
    public static FileWriter writer;
    private final Float rata;
    private final Long perioada;
    private Date data_deschidere;

    static {
        try {
            writer = new FileWriter("csv_db\\conturi_depozit.csv");
            writer.write("id,cnp_titular,valuta,sold,rata,perioada,data_deschidere\n");
        }
        catch (IOException e) {
            System.out.print("Error occured while creating FileWriter for ContDepozit.\n");
            e.printStackTrace();
        }
    }

    public static ContDepozit fromString(String s, HashMap<String, Client> hm_client) {
        String split[] = s.split(",");
        String cnp_titular = split[1];
        Client new_titular = hm_client.get(cnp_titular);
        return new ContDepozit(split[0], new_titular, split[2], split[3], split[4], split[5], split[6]);
    }

    public ContDepozit(Client titular, Float sold, String valuta, Float rata, Long perioada) {
        super(titular, valuta);
        this.sold = sold;
        this.rata = rata;
        this.perioada = perioada;
        data_deschidere = new Date();
    }

    public ContDepozit(String id, Client titular, String valuta, String sold, String rata, String perioada, String data_deschidere) {
        super(titular, valuta, id);
        this.rata = Float.parseFloat(rata);
        this.perioada = Long.parseLong(perioada);
        this.sold = Float.parseFloat(sold);
        DateFormat format = new SimpleDateFormat("E MMMM d kk:mm:ss zzzz yyyy");
        try {
            this.data_deschidere = format.parse(data_deschidere);
        }
        catch (ParseException e) {
            System.out.print("Error occured while parsing date from csv.\n");
            e.printStackTrace();
        }
    }

    public Float getRata() {
        return rata;
    }

    public Long getPerioada() {
        return perioada;
    }

    public Date getData_deschidere() {
        return data_deschidere;
    }

    public void updateSold() {
        Date now = new Date();
        if (now.getTime() - data_deschidere.getTime() >= perioada) {
            sold += sold * (rata / 100);
        }
    }

    public void lichidare(ContCurent c) {
        c.adaugaFonduri(sold, valuta);
        sold = 0f;
    }

    public void adaugaFonduri(Float fonduri, String sold) {
        System.out.println("Nu puteti adauga fonduri intr-un cont de depozit.");
    }

    public int retrageFonduri(Float fonduri, String sold) {
        System.out.println("Nu puteti retrage fonduri dintr-un cont de depozit.");
        return 0;
    }

    public void writeToFile() {
        try {
            writer.write(id + ',' + titular.getCNP() + ',' + valuta + ',' + sold + ',' + rata + ',' + perioada + ',' + data_deschidere + '\n');
            titular.writeToFile();
        }
        catch (IOException e) {
            System.out.print("Error occured while writing to file csv_db/conturi_depozit.csv.\n");
            e.printStackTrace();
        }
    }
}
