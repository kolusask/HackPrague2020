package hackprague.backend.quarkus;

import javax.enterprise.context.ApplicationScoped;
import javax.transaction.Transactional;
import javax.validation.Valid;

import hackprague.backend.quarkus.Order;

import static javax.transaction.Transactional.TxType.REQUIRED;
import static javax.transaction.Transactional.TxType.SUPPORTS;
import java.util.List;

@ApplicationScoped
@Transactional(REQUIRED)
public class OrderService {
    @Transactional(SUPPORTS)
    public List<Order> findAllOrders(){
        return Order.listAll();
    }

    @Transactional(SUPPORTS)
    public Order findOrderById(Long id){
        return Order.findById(id);
    }

    public Order persistOrder(@Valid Order order){
        Order.persist(order);
        return order;
    }

    public Order updateOrder(@Valid Order order){
        Order entity = Order.findById(order.id);

        entity.FreeTimeStart = order.FreeTimeStart;
        entity.FreeTimeEnd = order.FreeTimeEnd;
        entity.ClientID = order.ClientID;
        entity.FreelancerID = order.FreelancerID;
        entity.EstimatedHours = order.EstimatedHours;
        entity.EstimatedSalary = order.EstimatedSalary;
        entity.ProjectID = order.ProjectID;
        return entity;
    }

    public void deleteOrder(Long id){
        Order order = Order.findById(id);
        order.delete();
    }
    
}
