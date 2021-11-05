package aplicatie_bancara;

public class ConversieValuta {
    private String initiala;
    private String finala;
    private Float rata;

    public ConversieValuta(String initiala, String finala, Float rata) {
        this.initiala = initiala;
        this.finala = finala;
        this.rata = rata;
    }

    public String getInitiala() {
        return initiala;
    }

    public void setInitiala(String initiala) {
        this.initiala = initiala;
    }

    public String getFinala() {
        return finala;
    }

    public void setFinala(String finala) {
        this.finala = finala;
    }

    public Float getRata() {
        return rata;
    }

    public void setRata(Float rata) {
        this.rata = rata;
    }
}
