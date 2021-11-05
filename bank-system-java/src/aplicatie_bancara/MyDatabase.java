package aplicatie_bancara;

import java.sql.*;
import java.util.Scanner;
import java.util.HashMap;
import java.util.ArrayList;
import java.io.File;
import java.io.FileNotFoundException;

public class MyDatabase {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/bankapp_db";
    private static final String USER = "jdbc_user";
    private static final String PWD = "jdbc_pwd";
    private static Connection conn = null;

    private MyDatabase() {
    }

    private static ArrayList<String> getRowsAsCSV(String query, int cols_no) throws SQLException { 
        Statement stmt = conn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY);
        ResultSet resultSet = stmt.executeQuery(query);
        ArrayList<String> res = new ArrayList<>();
        while (resultSet.next()) {
            String row_csv = "";
            for (int i = 1; i <= cols_no - 1; i++) {
                row_csv += resultSet.getString(i) + ",";
            }
            row_csv += resultSet.getString(cols_no);
            res.add(row_csv);
        }
        return res;
    }

    public static Connection getConnection() {
        try {
            if (conn == null || conn.isClosed()) {
                conn = DriverManager.getConnection(DB_URL, USER, PWD);
            }
        }
        catch (SQLException e) {
            System.out.print("Error occured while getting a connection to the database.\n");
            e.printStackTrace();
        }
        return conn;
    }

    public static void closeConnection() {
        try {
            if (conn != null && !conn.isClosed()) {
                conn.close();
            }
        }
        catch (SQLException e) {
            System.out.print("Error occured while closing a connection to the database.\n");
            e.printStackTrace();
        }
    }

    public static void clearDatabase() {
        try {
            if (conn != null && !conn.isClosed()) {
                String base_sql = "truncate table ";
                String[] table_names = {"conturi_curente", "conturi_depozit", "tranzactii", "carduri", "clienti"};
                Statement stmt = conn.createStatement();
                for (int i = 0; i < table_names.length; i++) {
                    stmt.execute(base_sql + table_names[i] + ";");
                }
            }
        }
        catch (SQLException e) {
            System.out.print("Error occured while clearing database.\n");
            e.printStackTrace();
        }
    }

    public static void updateFromCSV() {
        try {
            if (conn != null && !conn.isClosed()) {
                String[] file_names = {"csv_db\\conturi_curente.csv", "csv_db\\conturi_depozit.csv", "csv_db\\tranzactii.csv", "csv_db\\carduri.csv", "csv_db\\clienti.csv"};
                String[] table_names = {"conturi_curente", "conturi_depozit", "tranzactii", "carduri", "clienti"};
                Statement stmt = conn.createStatement();
                String base_sql = "insert ignore into ";
                Scanner scanner = null;
                for (int i = 0; i < file_names.length; i++) {
                    scanner = new Scanner(new File(file_names[i]));
                    // column names in the database table must be the same as the header in the csv file
                    String header = scanner.nextLine();
                    String col_names = "(" + header + ")";
                    while (scanner.hasNextLine()) {
                        String[] line = scanner.nextLine().split(",");
                        // reading from csv the values for the sql insert statement
                        String value_tuple = "(";
                        for (int j = 0; j < line.length - 1; j++) {
                            value_tuple += "'" + line[j] + "'" + ",";
                        }
                        value_tuple += "'" + line[line.length - 1] + "'" + ")";
                        // insert ignore into table_name (col1_name, col2_name, ...) values (value1, value2, ...);
                        stmt.execute(base_sql + table_names[i] + " " + col_names + "values " + value_tuple + ";");
                    }
                }
                scanner.close();
                stmt.close();
            }
        }
        catch (SQLException e) {
            System.out.print("Error occured while updating database from CSV files.\n");
            e.printStackTrace();
        }
        catch (FileNotFoundException e) {
            System.out.print("Error occured while parsing CSV files for updating database.\n");
            e.printStackTrace();
        }
    }

    public static ArrayList<Cont> getConturi() {
        ArrayList<Cont> conturi = new ArrayList<>();
        try {
            HashMap<String, Client> hm_client = new HashMap<>();
            HashMap<String, Tranzactie> hm_tranzactie = new HashMap<>();
            HashMap<String, Card> hm_card = new HashMap<>();

            // conturi curente
            Statement stmt1 = conn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
            ResultSet set_conturi_curente = stmt1.executeQuery("select * from conturi_curente;");
            ArrayList<String> str_conturi_curente = getRowsAsCSV("select * from conturi_curente;", 6);
            while (set_conturi_curente.next()) {
                // adauga titularul contului in hash map daca nu este deja
                String CNP_client = set_conturi_curente.getString("cnp_titular");
                if (hm_client.get(CNP_client) == null) {
                    ArrayList<String> client_str = getRowsAsCSV("select * from clienti where CNP = '" + CNP_client + "';", 4);
                    hm_client.put(CNP_client, Client.fromString(client_str.get(0)));
                }
                
                // istoric tranzactii
                String[] istoric = set_conturi_curente.getString("vector_id_istoric").split(" ");
                for (int j = 0; j < istoric.length; j++) {
                    if (hm_tranzactie.get(istoric[j]) == null && !istoric[j].equals("empty")) {
                        ArrayList<String> str_tranzactie = getRowsAsCSV("select * from tranzactii where id = '" + istoric[j] + "';", 8);
                        hm_tranzactie.put(istoric[j], Tranzactie.fromString(str_tranzactie.get(0)));
                    }
                }
                
                // carduri
                String[] carduri = set_conturi_curente.getString("vector_id_carduri").split(" ");
                for (int j = 0; j < carduri.length; j++) {
                    if (hm_card.get(carduri[j]) == null && !carduri[j].equals("empty")) {
                        ArrayList<String> str_card = getRowsAsCSV("select * from carduri where numar = '" + carduri[j] + "';", 5);
                        hm_card.put(carduri[j], Card.fromString(str_card.get(0)));
                    }
                }

                conturi.add(ContCurent.fromString(str_conturi_curente.get(set_conturi_curente.getRow() - 1), hm_client, hm_tranzactie, hm_card));
            }
            set_conturi_curente.close();
            stmt1.close();

            // conturi depozit
            Statement stmt2 = conn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
            ResultSet set_conturi_depozit= stmt2.executeQuery("select * from conturi_depozit;");
            ArrayList<String> str_conturi_depozit = getRowsAsCSV("select * from conturi_depozit;", 7);
            while (set_conturi_depozit.next()) {
                // adauga titularul contului in hash map daca nu este deja
                String CNP_client = set_conturi_depozit.getString("cnp_titular");
                if (hm_client.get(CNP_client) == null) {
                    ArrayList<String> client_str = getRowsAsCSV("select * from clienti where CNP = '" + CNP_client + "';", 4);
                    hm_client.put(CNP_client, Client.fromString(client_str.get(0)));
                }

                conturi.add(ContDepozit.fromString(str_conturi_depozit.get(set_conturi_depozit.getRow() - 1), hm_client));
            }
            set_conturi_depozit.close();
            stmt2.close();
        }
        catch (SQLException e) {
            System.out.print("Error occured while joining tables to create needed data.\n");
            e.printStackTrace();
        }
        return conturi;
    }
}
