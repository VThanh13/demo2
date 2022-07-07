//NHAN VIEN
function addToStaffCart( flight_id, from, to, date_start, time_start, ticket_id, price, price_service, price_total, user_fullname, user_identify, user_phone) {
    fetch("/staff/api/add-item-cart", {
        method: 'post',
        body: JSON.stringify({
            "flight_id": flight_id,
            "from": from,
            "to": to,
            "date_start": date_start,
            "time_start": time_start,
            "ticket_id": ticket_id,
            "price": price,
            "price_service": price_service ,
            "price_total": price_total,
            "user_fullname": user_fullname,
            "user_identify": user_identify,
            "user_phone": user_phone
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById("cartCounter")
        if (counter !== null)
            counter.innerText = data.total_quantity
    })
    console.log("asdfsfsd")
}

function updateStaffCartItem(obj, flightId) {
    if(obj.value < 1  ) {
        obj.value = 1;
    }

    fetch("/staff/api/update-cart-item", {
        method: "put",
        body: JSON.stringify({
            "flight_id": flightId,
            "quantity": parseInt(obj.value)
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        if (data.error_code == 200) {

            const quantity = document.getElementById("cart-quantity")
            const amount = document.getElementById("cart-amount")
            const priceTicket = document.getElementById(`price-ticket-${flightId}`)
            const totalPriceTicket= document.getElementById(`total-ticket-${flightId}`)
            let d = data.cart_stats

            if (quantity !== null && amount !== null) {
                totalPriceTicket.innerText = Number(obj.value)* Number(priceTicket.innerText)
                quantity.innerText = d.total_quantity
                amount.innerText = d.total_amount
            }

            let counter = document.getElementById("cartCounter")
            if (counter !== null)
                counter.innerText = d.total_quantity
        } else
            alert("Cập nhật thất bại!")
    })


}


function staffPay() {
       fetch("/staff/api/pay", {
       confirm("CO XAC NHAN DAT VE CHO KHACH HANG ?")
           method: 'post'
       }).then(function(res) {
           return res.json()
       }).then(function(data) {
           if (data.error_code == 200)
               console.log("THANH TOAN THANH CONG")
           else
               alert("THANH TOAN DANG CO LOI!!! VUI LONG THUC HIEN SAU!")
       })
}
