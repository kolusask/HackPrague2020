package hackprague.backend.quarkus;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

import java.util.List;

//import hackprague.backend.quarkus.Customer;

import javax.persistence.Entity;
import javax.persistence.Column;
import javax.persistence.ManyToOne;
import javax.persistence.JoinColumn;
import javax.persistence.FetchType;


import javax.validation.constraints.NotNull;

import org.w3c.dom.Text;

@Entity
public class Review extends PanacheEntity{
    
    @NotNull
    public String Text;

    @NotNull
    public Double Mark;
   
    @Override
    public String toString(){
        return Text;
    }
}
