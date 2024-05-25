/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});



//var tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'INTC', 'PLTR', 'WCBR', 'SPY', 'ETH-USD', 'BTC-USD'];  // Array of stocks

function startUpdateCycle() { 
    updatePrices();
    setInterval(function () {
        updatePrices();                     // Update prices every minute
    }, 60000)
}

$(document).ready(function () {             // When document ready              // INDEX PAGE
    tickers.forEach(function (ticker) {
        addTickerToGrid(ticker);        
    });

    updatePrices();                         // Call updateprices

    startUpdateCycle();                     // Call price update 60s

    $('#add-ticker-form').submit(function (e) {
        e.preventDefault();
        var newTicker = $('#new-ticker').val().toUpperCase();
        if (!tickers.includes(newTicker)) {
            tickers.push(newTicker);
            localStorage.setItem('tickers', JSON.stringify(tickers))
            addTickerToGrid(newTicker);            
        }
        $('#new-ticker').val('');
        updatePrices();
    });
});



$(document).ready(function () {             // When document ready              // PORTFOLIO PAGE
    tickers.forEach(function (ticker) {
        addTickerToGrid2(ticker);        
    });

    updatePrices();                         // Call updateprices

    startUpdateCycle();                     // Call price update 60s

    $('#add-ticker-form2').submit(function (e) {
        e.preventDefault();
        var newTicker2 = $('#new-ticker2').val().toUpperCase();
        if (!tickers.includes(newTicker2)) {
            tickers.push(newTicker2);
            localStorage.setItem('tickers', JSON.stringify(tickers))
            addTickerToGrid2(newTicker2);            
        }
        $('#new-ticker2').val('');
        updatePrices();
    });

    $('#tickers-grid2').on('click', '.remove-btn', function () {         // click event listener for elements with class remove-btn
        var tickerToRemove = $(this).data('ticker');                    // When a user clicks the "Remove" button associated with a ticker, this function executes.
        tickers=tickers.filter(t => t !== tickerToRemove);              // It removes the ticker from the tickers array, updates the local storage, 
        localStorage.setItem('tickers', JSON.stringify(tickers))        // and removes the ticker from the grid.
        $(`#${tickerToRemove}`).remove();                               

    });
});



function addTickerToGrid(ticker) {
    $('#tickers-grid').append(`<div id="${ticker}" class="stock-box"><h2>${ticker}</h2><p id="${ticker}-price"></p><p id="${ticker}-pct"></p></div>`)
}                                                           // Function adds ticker box to html grid. ID, name, placeholder for price and % change

function addTickerToGrid2(ticker) {
    $('#tickers-grid2').append(`<div id="${ticker}" class="stock-box"><h2>${ticker}</h2><p id="${ticker}-price"></p><p id="${ticker}-pct"></p><button class="remove-btn" data-ticker="${ticker}">Remove</button></div>`)
}



function updatePrices() {
    tickers.forEach(function (ticker) {
        $.ajax({
            url: '/get_stock_data',
            type: 'POST',
            data: JSON.stringify({ 'ticker': ticker }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function (data) {
                var changePercent = ((data.currentPrice - data.openPrice) / data.openPrice) * 100;
                var colorClass;
                if (changePercent <= -2) {
                    colorClass = 'dark-red'
                } else if (changePercent < 0) {
                    colorClass = 'red'
                } else if (changePercent == 0) {
                    colorClass = 'gray'
                } else if (changePercent <= 2) {
                    colorClass = 'green'
                } else {
                    colorClass = 'dark-green'
                }

                $(`#${ticker}-price`).text(`$${data.currentPrice.toFixed(2)}`);
                $(`#${ticker}-pct`).text(`$${changePercent.toFixed(2)}%`);
                $(`#${ticker}-price`).removeClass('dark-red graz green dark-green').addClass(colorClass);
                $(`#${ticker}-pct`).removeClass('dark-red graz green dark-green').addClass(colorClass);
            }
        })
    })
}
