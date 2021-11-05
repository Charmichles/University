package aplicatie_bancara;

abstract class Cont implements Comparable<Cont> {
    public static Integer total_conturi;

    static {
        total_conturi = 0;
    }

    protected final String id;
    protected Client titular;
    protected String valuta;
    protected Float sold;

    public Cont(Client titular, String valuta) {
        this.titular = titular;
        total_conturi++;
        id = "cont" + total_conturi.toString();
        this.valuta = valuta;
    }

    public Cont(Client titular, String valuta, String id) {
        this.titular = titular;
        this.valuta = valuta;
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public Client getTitular() {
        return titular;
    }

    public void setTitular(Client titular) {
        this.titular = titular;
    }

    public String getValuta() {
        return valuta;
    }

    public void setValuta(String valuta) {
        this.valuta = valuta;
    }

    public Float getSold() {
        return sold;
    }

    public void setSold(Float sold) {
        this.sold = sold;
    }

    abstract public void adaugaFonduri(Float fonduri, String valuta);

    abstract public int retrageFonduri(Float fonduri, String valuta);

    abstract public void writeToFile();

    @Override
    public int compareTo(Cont c) {
        if (c.getTitular().getCNP().equals(titular.getCNP()))
            return 0;
        else if (c.getTitular().getCNP().compareTo(titular.getCNP()) < 0) {
            return 1;
        }
        else {
            return -1;
        }
    }

    @Override
    public String toString() {
        return "Cont{" +
                "id='" + id + '\'' +
                ", titular=" + titular +
                ", valuta='" + valuta + '\'' +
                ", sold=" + sold +
                '}';
    }
}
