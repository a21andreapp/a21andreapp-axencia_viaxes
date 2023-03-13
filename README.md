# Módulo axencia de viaxes

### DESCRICIÓN
A funcionalidade básica deste módulo é a xestión dunha empresa de axencia de viaxes. Dentro dela pódense crear tanto os destinos como os hoteis que desexan ofrecer, 
con esa información pódense crear os voos que van a ofrecer e a lista de actividades por destino que ofrecen.
Tamén se vai poder gardar a información de cada cliente dentro dos cales gardaremos o histórico de compras, e cos clientes e os datos anteriores podense gardar as compras de cada cliente.

### OBXECTIVOS
O principal obxectivo do módulo é a súa utilización para a xestión de empresas de axencia de viaxes.

### INSTRUCIÓN/DOCUMENTACIÓN DE USO
O módulo consta de 6 ventás, que son as seguintes:

    - Clientes: créanse e gárdanse os clientes. A vista principal é kanban pero tamén se poden visualizar en forma de árbore/lista. Os datos dos clientes que gardamos son os seguintes: nome, dni, teléfono, correo electrónico, data de nacemento e a idade. O campo idade é calculado de forma automática a través da data de nacemento, o campo dni, teléfono e correo electrónico ten unha función que comproba se se introduce de forma correcta conforme a un patrón. Nesta vista, tamén se visualizan as compras realizadas polo cliente

    - Destinos: créanse e gárdanse os lugares de destino que a empresa pode ofrecer. A vista principal e única deste modelo é a vista de árbore/lista. Os campos definidos neste modelo son id, creado automáticamente, destino e aeroporto. Dispón dun botón, que é o seguinte:

        - Borrar destino: permite borrar un destino.

    - Voos: créanse e gárdanse os voos ofrecidos pola compañía. A vista principal é a de árbore/lista, pero tamén se pode visualizar ca vista de calendario e a vista kanban, na cal están agrupados según o estado no que se atope o voo. Os campos definidos neste modelo son os seguintes: lugar de saída e lugar de chegada, ambos como un campo relacional do modelo destino, número de escalas, lugares de escalas, no cal simplemente se escriben os lugares onde se fai escala separado por guión, hora de ida e hora de chegada e o prezo do voo.
    Compróbase que a hora de ida non é igual á hora actual nin un día futuro e que a hora de chegada non é antes da hora de ida.
    Dispoñemos dos seguintes botóns: 

        - Cancelado: cambia o estado do voo a cancelado.
        
        - Rematado: cambia o estado do voo a rematado cando a data de chegada sexa igual ou inferior á data e hora actual.
        
        - Agotado: cambia o estado do voo a agotado.
        
        - Dispoñible: cambia o estado do voo a dispoñible.

        - Borrar voo: permite borrar un voo.

    O estado dos voos pode cambiar de dispoñible -> rematado, dispoñible -> cancelado, dispoñible -> agotado, cancelado -> dispoñible, agotado -> dispoñible, agotado -> rematado.

    - Actividades: créanse e gárdanse novas actividades agrupadas según o destino onde se realizan, nela gárdase información como o nome da actividade, breve descrición da actividade, número de persoas mínimas necesarias para a realización da actividade, o destino/lugar onde se realiza a actividade e o prezo da actividade. A súa vista principal é kanban para poder visualizalas agrupadas polo destino pero tamén e posible velas en modo árbore. Dispoñemos do seguinte botón:

        - Borrar actividade: borra a actividade selecionada.

    - Hoteles: créanse e gárdanse os hoteis cos que a empresa traballa e que ofrece a os seus clientes. A única vista da que dispón é da vista árbore/lista. Os campos que conforman esta vista son: nome do hotel, ubicación, cidade, para poder relacionala cun destino, e o prezo por noite. Dispón do seguinte botón:

        - Borrar hotel: permite borrar un hotel.

    - Ventas: créanse e gárdanse as ventas realizadas. A vista que ofrece é a de árbore/lista. Os campos que emprega son: cliente, que é un campo relacionado co modelo cliente, vuelo, que tamén é un campo relacionado co modelo vuelo, número de días, data de compra, que se pon automáticamente co día actual no que se realiza a venta, pagado, que é un booleano que indica se se realizou o pago, prezo o cal é calculado según o prezo total do hotel, é dicir o número de días escollidos e o prezo do hotel por noite, o prezo total das actividades escollidas e o prezo do voo e a lista de actividades que mercou.
    No caso de que un cliente intente realizar unha compra e teña algunha sen pagar non deixa realizar a venta.