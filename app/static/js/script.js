function addToCart( flight_id, type_id, type_name, from, to, date_start, time_start, ticket_id, price, price_service, price_total ) {
    fetch("/api/add-item-cart", {
        method: 'post',
        body: JSON.stringify({
            "flight_id": flight_id,
            "type_id": type_id,
            "type_name": type_name,
            "from": from,
            "to": to,
            "date_start": date_start,
            "time_start": time_start,
            "ticket_id": ticket_id,
            "price": price,
            "price_service": price_service ,
            "price_total": price_total,
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
}

function updateCartItem(obj, ticketId) {
    if(obj.value < 1  ) {
        obj.value = 1;
    }

    fetch("/api/update-cart-item", {
        method: "put",
        body: JSON.stringify({
            "ticket_id": ticketId,
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
            const priceTicket = document.getElementById(`price-ticket-${ticketId}`)
            const totalPriceTicket= document.getElementById(`total-ticket-${ticketId}`)
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

function deleteCartItem(ticketId) {
    if (confirm("Bạn có chắc chắn xóa chuyến bay này không?") == true) {
        fetch("/api/delete-cart-item/" + ticketId, {
            method: "delete"
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            if (data.error_code == 200) {
                let quantity = document.getElementById("cart-quantity")
                let amount = document.getElementById("cart-amount")
                if (quantity !== null && amount !== null) {
                    let d = data.cart_stats
                    quantity.innerText = d.total_quantity
                    amount.innerText = d.total_amount

                     let counter = document.getElementById("cartCounter")
                    if (counter !== null)
                        counter.innerText = d.total_quantity

//                    location.reload()
                    let row = document.getElementById("ticket" + ticketId)
                    row.style.display = "none"
                }
            } else
                alert("Xóa thất bại!")
        })
    }
}


function pay() {
       fetch("/api/pay", {
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

function staffPay() {
        confirm("CO XAC NHAN DAT VE CHO KHACH HANG ?")
       fetch("/staff/api/pay", {
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

// FUNCTION MODIFIER
function changePrice() {
        const lbTg = document.querySelector("#service-tg")
        const lbPt = document.querySelector("#service-pt")
        const url = window.location.search
        let a = url
        a = a.split("&")
        if (a[1] === "type=Vip" || a[1] === "type=VIP") {
            lbTg.classList.add("sd")
        }
        if(a[1] === "type=Normal" || a[1] === "type=NORMAL") {
            lbPt.classList.add("sd")
        }
}

function confirmDelete() {
    confirm("BẠN CÓ CHẮC CHẮN MUỐN XÓA KHÁCH HÀNG NÀY")
}

function checkPay() {
    const money = document.getElementById("cart-money")
    const excess = document.getElementById("cart-excess")
    const amount = document.getElementById("cart-amount")
    console.log(Number(money.value), Number(amount.innerText))
    if ( Number(money.value) < Number(amount.innerText) ) {
        excess.innerText = ""
        alert("KHÁCH HÀNG CHƯA TRẢ ĐỦ TIỀN")
    } else {
        excess.innerText = Number(money.value) - Number(amount.innerText)
    }
}


function changeFollow() {
    const changeFl = document.getElementById("pro")
    changeFl.innerText = "Khách hàng thân quen"
    classList.add("color-bl")
}
