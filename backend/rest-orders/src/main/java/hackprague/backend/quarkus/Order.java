package hackprague.backend.quarkus;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

import java.util.List;
import java.util.Set;
import java.util.Date;

import javax.persistence.Entity;

import javax.validation.constraints.NotNull;

@Entity
public class Order extends PanacheEntity{

    @NotNull
    public Date FreeTimeStart;
    @NotNull 
    public Date FreeTimeEnd;
    @NotNull
    public Double EstimatedSalary;
    @NotNull
    public Long EstimatedHours;

    //disclaimer: yes, I know that here should be foreign keys
    //but I'm kinda new to Quarkus and Java itself...
    @NotNull
    public Long FreelancerID;
    @NotNull
    public Long ClientID;
    @NotNull
    public Long ProjectID;

    @Override
    public String toString(){
        return "";
    }
}
