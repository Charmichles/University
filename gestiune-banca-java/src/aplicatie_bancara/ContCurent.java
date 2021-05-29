package aplicatie_bancara;

import java.util.ArrayList;
import java.util.Date;
import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class ContCurent extends Cont{

    private static ArrayList<ConversieValuta> rate_conversie;
    public static FileWriter writer;
    private ArrayList<Tranzactie> istoric;
    private ArrayList<Card> carduri;

    static {
        rate_conversie = new ArrayList<>();
        try {
            writer = new FileWriter("csv_db\\conturi_curente.csv");
            writer.write("id,cnp_titular,valuta,sold,vector_id_istoric,vector_id_carduri\n");
        }
        catch (IOException e) {
            System.out.print("Error occured while creating FileWriter for ContCurent.\n");
            e.printStackTrace();
        }
        addRataConversie(new ConversieValuta("lei", "euro", 0.25f));
        addRataConversie(new ConversieValuta("euro", "lei", 4f));
        addRataConversie(new ConversieValuta("lei", "lei", 1f));
        addRataConversie(new ConversieValuta("euro", "euro", 1f));
    }

    public static ContCurent fromString(String s, HashMap<String, Client> hm_client, HashMap<String, Tranzactie> hm_tranz, HashMap<String, Card> hm_card)
    {
        String split[] = s.split(",");
        String cnp_titular = split[1];
        String[] id_tranzactii = null;
        if (split.length >= 5) {
            id_tranzactii = split[4].split(" ");
        }
        else {
            id_tranzactii = new String[0];
        }
        String[] id_carduri = null;
        if (split.length >= 6) {
            id_carduri = split[5].split(" ");
        }
        else {
            id_carduri = new String[0];
        }
        Client new_titular = hm_client.get(cnp_titular);
        ArrayList<Tranzactie> new_istoric = new ArrayList<>();
        ArrayList<Card> new_carduri = new ArrayList<>();
        for (int i = 0; i < id_tranzactii.length; i++) {
            new_istoric.add(hm_tranz.get(id_tranzactii[i]));
        }
        for (int i = 0; i < id_carduri.length; i++) {
            new_carduri.add(hm_card.get(id_carduri[i]));
        }
        return new ContCurent(split[0], new_titular, split[2], split[3], new_istoric, new_carduri);
    }

    public ContCurent(Client titular, String valuta) {
        super(titular, valuta);
        sold = 0f;
        istoric = new ArrayList<>();
        carduri = new ArrayList<>();
    }

    public ContCurent(String id, Client titular, String valuta, String sold, ArrayList<Tranzactie> istoric, ArrayList<Card> carduri)
    {
        super(titular, valuta, id);
        this.sold = Float.parseFloat(sold);
        this.istoric = istoric;
        this.carduri = carduri;
    }

    public static void addRataConversie(ConversieValuta c) {
        rate_conversie.add(c);
    }

    public static void setRataConversie(ConversieValuta c, Float rata) {
        for (ConversieValuta conversieValuta : rate_conversie) {
            if (c.getInitiala().equals(conversieValuta.getInitiala()) && c.getFinala().equals(conversieValuta.getFinala())) {
                conversieValuta.setRata(rata);
                break;
            }
        }
    }

    public void adaugaFonduri(Float fonduri, String valuta) {
        for (ConversieValuta c : rate_conversie) {
            if (c.getInitiala().equals(valuta) && c.getFinala().equals(this.valuta)) {
                this.sold += fonduri * c.getRata();
                break;
            }
        }
    }

    public int retrageFonduri(Float fonduri, String valuta) {
        // Return values: 0, daca sunt destule fonduri, altfel -1
        for (ConversieValuta c : rate_conversie) {
            if (c.getInitiala().equals(valuta) && c.getFinala().equals(this.valuta)) {
                if (this.sold - fonduri * c.getRata() >= 0) {
                    this.sold -= fonduri * c.getRata();
                    break;
                }
                else {
                    return -1;
                }
            }
        }
        return 0;
    }

    public ArrayList<Tranzactie> getIstoric() {
        return istoric;
    }

    public void setIstoric(ArrayList<Tranzactie> istoric) {
        this.istoric = istoric;
    }

    public void addTranzactie(Tranzactie t) {
        this.istoric.add(t);
    }

    public String getIstoricStr() {
        String istoric_str = "";
        for (Tranzactie t : istoric) {
            istoric_str += t;
            istoric_str += '\n';
        }
        return istoric_str;
    }

    public ArrayList<Card> getCarduri() {
        return carduri;
    }

    public String getCarduriStr() {
        String carduri_str = "";
        for (Card c : carduri) {
            carduri_str += c;
            carduri_str += '\n';
        }
        return carduri_str;
    }

    public void setCarduri(ArrayList<Card> carduri) {
        this.carduri = carduri;
    }

    public void addCard(Card c) {
        this.carduri.add(c);
    }

    public void creeazaCard() {
        Date date = new Date();
        date.setTime(date.getTime() + (long)Math.pow(3, 10));
        Random rand = new Random();
        Integer CVV = rand.nextInt(900) + 100;
        Integer PIN = rand.nextInt(9000) + 1000;
        Card c = new Card(id + "card" + carduri.size(), date, CVV, titular.getNume(), PIN);
        addCard(c);
    }

    public void writeToFile() {
        try {
            String vector_id_istoric = "";
            String vector_id_carduri = "";
            for (Tranzactie t : istoric) {
                if (t != null) {
                    vector_id_istoric += t.getId() + ' ';
                    t.writeToFile();
                }
            }
            for (Card c : carduri) {
                if (c != null) {
                    vector_id_carduri += c.getNumar() + ' ';
                    c.writeToFile();
                }
            }
            if (vector_id_istoric.equals("")) {
                vector_id_istoric = "empty";
            }
            if (vector_id_carduri.equals("")) {
                vector_id_carduri = "empty";
            }
            writer.write(id + ',' + titular.getCNP() + ',' + valuta + ',' + sold + ',' + vector_id_istoric + ',' + vector_id_carduri + '\n');
            titular.writeToFile();
        }
        catch (IOException e) {
            System.out.print("Exception occured while writing to file csv_db/conturi_curente.csv.\n");
            e.printStackTrace();
        }
    }
}
