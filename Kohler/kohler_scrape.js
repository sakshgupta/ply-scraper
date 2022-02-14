const puppeteer = require('puppeteer');
let fs = require('fs');

async function getdetails(url, page){
    try{
        await page.goto(url);
    
        // Name
        const prod_name = await page.$eval(".koh-product-short-description", div => div.textContent);
    
        // Code
        const code = await page.$eval(".koh-product-skus-colors .koh-product-sku", span => span.textContent);
    
        // Price
        const price = await page.$eval("#koh-page-outer > div > div.koh-page > section > div.koh-product-top-row > div.koh-product-details > div.koh-product-skus-colors > ul > li > span", span => span.textContent);
        
        let temp1 = price.replace(/,/g, ".");
    
        // Color Name
        const color = [];
        const img = [];
        const lis = await page.$$(".koh-product-colors > ul > li > span");
    
        for(let i =0; i<lis.length;i++){
            // Click
            lis[i].click();
            // Color
            color.push(await page.$eval(".koh-product-colors > span.koh-product-colors-selected", span => span.innerText));
            // Image
            img.push(await page.$eval("img.koh-product-iso-image", img => img.src));
    
            await page.waitForTimeout((Math.floor(Math.random()*3)+1)*1000);
        }

        let temp2 = color.toString();
        temp2= temp2.replace(/,/g, " ");
        let temp3 = img.toString();
        temp3= temp3.replace(/,/g, "    ");

        // To csv
        if (prod_name !== "Null") {
            fs.appendFile(
                "result.csv",
                `${url}, ${prod_name}, ${code}, ${temp1}, ${temp2}, ${temp3}\n`,
                function (err) {
                    if (err) throw err;
                }
                );
        }
    
        return {
            URL: url,
            Name: prod_name,
            Code: code,
            Price: price,
            Color_Name: color,
            Image_Link: img
        };
    }
    catch(e){
        throw e;
    }
};

async function getLinks(page){
    let links=[];

    await page.goto("https://www.kohler.co.in/browse/Bathroom/Basin");

    links = await page.$$eval('.koh-product-tile-inner .koh-product-tile-content a', allAs => allAs.map(a => a.href));

    return links;
}


async function main(){
    const browser = await puppeteer.launch({headless: false, defaultViewport: false});
    const page = await browser.newPage();

    const alldata = [];
    const allLinks = await getLinks(page);
    let i=0;

    for(let link of allLinks){
        const data = await getdetails(link,page);
        alldata.push(data);
        // if(i==3) break;
        // i++;
    }
    console.log(alldata);
    console.log("Converted to excel file");
    console.log("Done!!");

    await browser.close()
}

main();

// Code by Saksham Gupta