package aplicatie_bancara;

import java.util.ArrayList;
import java.util.Scanner;
import java.io.FileWriter;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.io.IOException;
import java.io.File;
import java.io.FileNotFoundException;
import java.text.ParseException;

public class Admin {
    private static FileWriter audit_writer;
    private static ArrayList<Cont> conturi;
    private static final ArrayList<String> optiuni;
    private static final ArrayList<Cont> conturi_utilizator_curent;
    private static Client utilizator_curent;
    private static Scanner keyboard = new Scanner(System.in);

    static {
        conturi = new ArrayList<>();
        optiuni = new ArrayList<>();
        conturi_utilizator_curent = new ArrayList<>();
        optiuni.add("1. Creeaza un cont curent.\n");
        optiuni.add("2. Creeaza un cont de depozit.\n");
        optiuni.add("3. Adauga bani intr-un cont curent.\n");
        optiuni.add("4. Retrage bani dintr-un cont curent.\n");
        optiuni.add("5. Efectueaza o tranzactie cu un alt cont curent.\n");
        optiuni.add("6. Creeaza un card.\n");
        optiuni.add("7. Istoric tranzactii.\n");
        optiuni.add("8. Detalii cont.\n");
        optiuni.add("9. Detalii client.\n");
        optiuni.add("10. Inchidere cont.\n");
        optiuni.add("11. Iesire.\n");
        try {
            audit_writer = new FileWriter(new File("audit.csv"));
            audit_writer.write("nume_actiune,timestamp\n");
        }
        catch (IOException e) {
            System.out.print("Exception occured while creating FileWriter for audit.csv.\n");
            e.printStackTrace();
        }
    }

    private Admin() {

    }

    private static void citesteCSV() throws ParseException {
        HashMap<String, Tranzactie> hashmap_tranzactii = new HashMap<String, Tranzactie>();
        HashMap<String, Card> hashmap_carduri = new HashMap<String, Card>();
        HashMap<String, Client> hashmap_clienti = new HashMap<String, Client>();
        // formarea hash map-ul cu tranzactii cu cheia id-ul tranzactiei si valoarea un obiect Tranzactie instantiat
        // se va folosi pentru a completa istoricul de tranzactii pentru fiecare ContCurent
        try {
            Scanner scanner_tranzactii = new Scanner(new File("csv_db\\tranzactii.csv"));
            scanner_tranzactii.nextLine();
            while (scanner_tranzactii.hasNextLine()) {
                String str_tranzactie = scanner_tranzactii.nextLine();
                String id_tranzactie = str_tranzactie.split(",")[0];
                hashmap_tranzactii.put(id_tranzactie, Tranzactie.fromString(str_tranzactie));
            }
            scanner_tranzactii.close();
        }
        catch (FileNotFoundException e) {
            System.out.print("Error occured while reading from file csv_db\\tranzactii.csv.\n");
            e.printStackTrace();
        }
        // formarea hash map-ul cu carduri cu cheia numele cardului si valoarea un obiect Card instantiat
        // se va folosi pentru a completa lista de carduri pentru fiecare ContCurent
        try {
            Scanner scanner_carduri = new Scanner(new File("csv_db\\carduri.csv"));
            scanner_carduri.nextLine();
            while (scanner_carduri.hasNextLine()) {
                String str_card = scanner_carduri.nextLine();
                String id_card = str_card.split(",")[0];
                hashmap_carduri.put(id_card, Card.fromString(str_card));
            }
            scanner_carduri.close();
        }
        catch (FileNotFoundException e) {
            System.out.print("Error occured while reading from file csv_db\\carduri.csv.\n");
            e.printStackTrace();
        }
        // formarea hash map-ul cu clienti cu cheia CNP-ul clientului si valoarea un obiect Client instantiat
        // se va folosi pentru a completa campul titular pentru fiecare Cont
        try {
            Scanner scanner_clienti = new Scanner(new File("csv_db\\clienti.csv"));
            scanner_clienti.nextLine();
            while (scanner_clienti.hasNextLine()) {
                String str_client = scanner_clienti.nextLine();
                String id_client = str_client.split(",")[1];
                hashmap_clienti.put(id_client, Client.fromString(str_client));
            }
            scanner_clienti.close();
        }
        catch (FileNotFoundException e) {
            System.out.print("Error occured while reading from file csv_db\\clienti.csv.\n");
            e.printStackTrace();
        }
        // formarea listei de conturi cu toate informatiile necesare folosind hash map-urile generate anterior
        ArrayList<Cont> conturi_csv = new ArrayList<Cont>();
        // adaugarea conturilor curente
        try {
            Scanner scanner_conturi_curente = new Scanner(new File("csv_db\\conturi_curente.csv"));
            scanner_conturi_curente.nextLine();
            while (scanner_conturi_curente.hasNextLine()) {
                String str_cont = scanner_conturi_curente.nextLine();
                conturi_csv.add(ContCurent.fromString(str_cont, hashmap_clienti, hashmap_tranzactii, hashmap_carduri));
            }
        }
        catch (FileNotFoundException e) {
            System.out.print("Error occured while reading from file csv_db\\conturi_curente.csv.\n");
            e.printStackTrace();
        }
        // adaugarea conturilor depozit
        try {
            Scanner scanner_conturi_depozit = new Scanner(new File("csv_db\\conturi_depozit.csv"));
            scanner_conturi_depozit.nextLine();
            while (scanner_conturi_depozit.hasNextLine()) {
                String str_cont = scanner_conturi_depozit.nextLine();
                conturi_csv.add(ContDepozit.fromString(str_cont, hashmap_clienti));
            }
        }
        catch (FileNotFoundException e) {
            System.out.print("Error occured while reading from file csv_db\\conturi_depozit.csv.\n");
            e.printStackTrace();
        }
        // sorteaza dupa cnp
        Collections.sort(conturi_csv);
        // actualizeaza informatia
        for (Cont c : conturi_csv) {
            conturi.add(c);
        }
        Cont.total_conturi = conturi.size();
    }

    private static void scrieCSV() {
        for (Cont c : conturi) {
            if (c != null) {
                c.writeToFile();
            }
        }
        try {
            ContDepozit.writer.close();
            ContCurent.writer.close();
            Tranzactie.writer.close();
            Card.writer.close();
            Client.writer.close();
            audit_writer.close();
        }
        catch (IOException e) {
            System.out.print("Exception occured while closing FileWriter objects for all classes.\n");
            e.printStackTrace();
        }
    }

    private static Cont getCont(ArrayList<Cont> arr_conturi, String id) {
        for (Cont c : arr_conturi) {
            if (id.equals(c.getId())) {
                return c;
            }
        }
        if (arr_conturi == conturi) {
            System.out.print("ID-ul introdus este gresit sau contul nu exista!\n");
        }
        else if (arr_conturi == conturi_utilizator_curent) {
            System.out.print("ID-ul introdus este gresit sau contul nu va apartine!\n");
        }
        return null;
    }

    private static void creeazaCont(String tip) {
        switch (tip) {
            case "curent" -> {
                Cont c = new ContCurent(utilizator_curent, "lei");
                conturi.add(c);
                conturi_utilizator_curent.add(c);
            }
            case "depozit" -> {
                System.out.print("Din ce cont doriti sa retrageti fonduri pentru a deschide un depozit? ID:\n");
                Cont cont_ales = getCont(conturi_utilizator_curent, keyboard.nextLine());
                if (cont_ales == null)
                    creeazaCont(tip);
                else {
                    System.out.print("Ce suma ati dori sa retrageti? Suma:\n");
                    Float suma_aleasa = Float.parseFloat(keyboard.nextLine());
                    Float sold_vechi = cont_ales.getSold();
                    if (cont_ales.retrageFonduri(suma_aleasa, "lei") != -1) {
                        Cont c = new ContDepozit(utilizator_curent, suma_aleasa, "lei", 1f, (long) 3e10);
                        ContCurent aux = (ContCurent) cont_ales;
                        aux.addTranzactie(new Tranzactie(aux, aux, "lei", suma_aleasa, "Creeare depozit", sold_vechi));
                        conturi.add(c);
                        conturi_utilizator_curent.add(c);
                    } else {
                        System.out.print("Nu exista destule fonduri pentru a creea un depozit.\n");
                    }
                }
            }
            default -> System.out.print("Tipul de cont introdus este gresit.\n");
        }
    }

    private static void efectueazaTranzactie(String tip) {
        System.out.print("Alegeti un cont pentru efectuarea tranzactiei. ID:\n");
        Cont cont_ales = getCont(conturi_utilizator_curent, keyboard.nextLine());
        if (cont_ales == null) {
            efectueazaTranzactie(tip);
        }
        else {
            System.out.print("Ce suma doriti sa ");
            switch (tip) {
                case "self_adauga" -> {
                    System.out.print("adaugati la cont? Suma:\n");
                    Float suma_aleasa = Float.parseFloat(keyboard.nextLine());
                    ContCurent aux = (ContCurent) cont_ales;
                    aux.addTranzactie(new Tranzactie(aux, aux, "lei", suma_aleasa, "Alimentare cont", aux.getSold()));
                    cont_ales.adaugaFonduri(suma_aleasa, "lei");
                }

                case "self_retrage" -> {
                    System.out.print("retrageti din cont? Suma:\n");
                    Float suma_aleasa = Float.parseFloat(keyboard.nextLine());
                    if (cont_ales instanceof ContCurent) {
                        ContCurent aux = (ContCurent) cont_ales;
                        Float sold_vechi = aux.getSold();
                        if (aux.retrageFonduri(suma_aleasa, "lei") != -1) {
                            aux.addTranzactie(new Tranzactie(aux, aux, "lei", suma_aleasa, "Retragere din cont" , sold_vechi));
                        }
                        else {
                            System.out.print("Nu exista destule fonduri disponibile.\n");
                        }
                    }
                    else {
                        System.out.print("Nu se pot retrage fonduri dintr-un cont de depozit.\n");
                    }
                }

                case "tranzactie" -> {
                    System.out.print(" transferati? Suma:\n");
                    Float suma_aleasa = Float.parseFloat(keyboard.nextLine());
                    System.out.print("Catre ce cont doriti sa transferati? ID:\n");
                    Cont cont_transfer = getCont(conturi, keyboard.nextLine());
                    System.out.print("Ce mesaj doriti sa aiba tranzactia? Mesaj:\n");
                    String mesaj = keyboard.nextLine();
                    Tranzactie t = new Tranzactie((ContCurent) cont_ales, (ContCurent) cont_transfer, "lei", suma_aleasa, mesaj, cont_transfer.getSold());
                    t.efectueazaTranzactie((ContCurent) cont_ales, (ContCurent) cont_transfer);
                }

                default -> System.out.print("Tipul de tranzactie introdusa este gresita!\n");
            }
        }
    }

    private static void creeazaCard() {
        System.out.print("Pentru care cont doriti sa creeati un card? ID:\n");
        Cont cont_ales = getCont(conturi_utilizator_curent, keyboard.nextLine());
        if (cont_ales == null) {
            creeazaCard();
        }
        else if (cont_ales instanceof ContDepozit) {
            System.out.print("Nu se poate creea un card pentru un cont de depozit. Va rugam alegeti un cont curent.\n");
            creeazaCard();
        }
        else {
            ContCurent aux = (ContCurent) cont_ales;
            aux.creeazaCard();
            System.out.print("Card creeat cu succes. Folositi comanda 'Detalii cont' pentru a vedea informatii despre carduri.\n");
        }
    }

    private static void printDetalii(String tip) {
        switch (tip) {
            case "istoric" -> {
                System.out.print("Pentru ce cont doriti sa vizualizati istoricul? ID:\n");
                Cont cont_ales = getCont(conturi_utilizator_curent, keyboard.nextLine());
                if (cont_ales instanceof ContCurent) {
                    ContCurent aux = (ContCurent) cont_ales;
                    System.out.print(aux.getIstoricStr() + '\n');
                }
                else if (cont_ales != null) {
                    System.out.print("Nu se poate vizualiza istoricul pentru un cont depozit.\n");
                }
            }
            case "cont" -> {
                System.out.print("Pentru ce cont doriti sa vizualizati detalii? ID:\n");
                Cont cont_ales = getCont(conturi_utilizator_curent, keyboard.nextLine());
                System.out.println(cont_ales);
                if (cont_ales instanceof ContCurent) {
                    ContCurent aux = (ContCurent) cont_ales;
                    System.out.print("Carduri:\n" + aux.getCarduriStr() + '\n');
                }
                else if (cont_ales instanceof ContDepozit) {
                    ContDepozit aux = (ContDepozit) cont_ales;
                    System.out.print("Cont depozit cu rata: " + aux.getRata() + " si perioada: " + aux.getPerioada() + " deschis la data: " + aux.getData_deschidere() + '\n');
                }
            }
            case "client" -> {
                System.out.print(utilizator_curent);
            }
            default -> System.out.print("Nu se pot afisa detalii pentru tipul introdus.\n");
        }
    }

    private static void inchideCont() {
        System.out.print("Ce cont doriti sa inchideti? ID:\n");
        Cont cont_ales = getCont(conturi_utilizator_curent, keyboard.nextLine());
        if (cont_ales == null) {
            System.out.print("Contul ales nu exista sau nu va apartine.\n");
            inchideCont();
        }
        else {
            conturi.remove(cont_ales);
            conturi_utilizator_curent.remove(cont_ales);
        }
    }

    private static void printMeniu() {
        for (String o : optiuni) {
            System.out.print(o);
        }
    }

    private static void printFarewell() {
        System.out.print("Va multumim pentru ca ati ales banca noastra! O zi buna!\n");
    }

    private static void printConturi(ArrayList<Cont> arr_conturi) {
        for (Cont c : arr_conturi) {
            if (c instanceof ContCurent) {
                System.out.print("Cont curent: ");
            }
            else if (c instanceof ContDepozit) {
                System.out.print("Cont depozit: ");
            }
            System.out.println(c.toString());
        }
    }

    private static void interogareClient() {
        utilizator_curent = Client.citesteClient(keyboard);
        conturi_utilizator_curent.clear();
        for (Cont c : conturi) {
            if (c.getTitular().equals(utilizator_curent)) {
                conturi_utilizator_curent.add(c);
            }
        }
        int option_idx = 0;
        do {
            printMeniu();
            System.out.print("Conturile dumneavoastra:\n");
            printConturi(conturi_utilizator_curent);
            System.out.print("Alegeti operatie:\n");
            try {
                option_idx = Integer.parseInt(keyboard.nextLine());
            }
            catch (Exception e) {
                System.out.print("Trebuie introdus un numar de la 1 la 11.\n");
            };
            switch (option_idx) {
                case 1 -> creeazaCont("curent");
                case 2 -> creeazaCont("depozit");
                case 3 -> efectueazaTranzactie("self_adauga");
                case 4 -> efectueazaTranzactie("self_retrage");
                case 5 -> efectueazaTranzactie("tranzactie");
                case 6 -> creeazaCard();
                case 7 -> printDetalii("istoric");
                case 8 -> printDetalii("cont");
                case 9 -> printDetalii("client");
                case 10 -> inchideCont();
                case 11 -> printFarewell();
                default -> System.out.print("Numarul optiunii a fost introdus gresit.\n");
            }
            try {
                if (option_idx >= 1 && option_idx <= 11) {
                    audit_writer.write(option_idx + ',' + (new Date()).toString());
                }
            }
            catch (IOException e) {
                System.out.print("Error occured while writing to audit.csv.\n");
                e.printStackTrace();
            }
        } while (option_idx != 11);
    }

    public static void startProgram() {
        System.out.print("Bine ati venit la banca noastra!\n");
        while(true) {
            System.out.print("Pentru a continua executia introduceti orice. Pentru a opri scrieti 'stop'\n");
            if (keyboard.nextLine().equals("stop")) {
                break;
            }
            Admin.interogareClient();
        }
        keyboard.close();
    }

    public static void startProgramCSV() {
        try {
            Admin.citesteCSV();
        }
        catch (ParseException e) {
            System.out.print("Error occured while parsing csv files.\n");
            e.printStackTrace();
        }
        Admin.startProgram();
        Admin.scrieCSV();
    }

    public static void startProgramJDBC() {
        MyDatabase.getConnection();
        conturi = MyDatabase.getConturi();
        Cont.total_conturi = conturi.size();
        Admin.startProgram();
        MyDatabase.clearDatabase();
        Admin.scrieCSV();
        MyDatabase.updateFromCSV();
        MyDatabase.closeConnection();
    }
}
