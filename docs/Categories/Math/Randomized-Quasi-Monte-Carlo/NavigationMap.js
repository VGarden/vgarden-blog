var NavigationMap = (function() {

    const __roman_table = [
        [1000,  "M"],
        [ 900, "CM"],
        [ 500,  "D"],
        [ 400, "CD"],
        [ 100,  "C"],
        [  90, "XC"],
        [  50,  "L"],
        [  40, "XL"],
        [  10,  "X"],
        [   9, "IX"], 
        [   5,  "V"],
        [   4, "IV"],
        [   1,  "I"]
    ];
    const __number_to_roman = x => {
        let symbols = [];
        for(let [value, symbol] of __roman_table)
            while(x >= value) {
                x -= value;
                symbols.push(symbol);
            }
        return symbols.join("")
    };

    function NavigationMap() {
        this.__NavigationMap_uuidsKeeper = {
            uuids: {},
            newUuid: function() {
                let uuid; do {
                    uuid = Math.floor(Math.random()*1000000000);
                } while(this.uuids[uuid]);
                this.uuids[uuid] = true;
                return "NavigationMap_" + uuid;
            }
        };
    }


    NavigationMap.prototype = {
        __NavigationMap_uuidsKeeper: undefined, // In constructor
        convertTitleToLink: function(textContent, { titleElement, liElement }) {
            let anchor = document.createElement("a");
            let link = document.createElement("a");
            let uuid = this.__NavigationMap_uuidsKeeper.newUuid();

            anchor.setAttribute("name", uuid);
            link.setAttribute("href", "#"+uuid);

            textContent = textContent || (titleElement && titleElement.textContent);

            anchor.textContent = textContent;
            link.textContent = textContent;

            if(titleElement) {
                titleElement.innerHTML = "";
                titleElement.appendChild(anchor);
            }
            if(liElement) {
                liElement.innerHTML = "";
                liElement.appendChild(link);
            }
            
            return { anchor, link };
        },
        createRomanCounterElement: function(decimalCounters, { target, classList }) {
            let element = document.createElement("span");
            element.textContent = decimalCounters
                                .map(__number_to_roman)
                                .join(".") + (". ");

            if (target) {
                target.insertBefore(element, target.firstElementChild);
            }

            if (classList) {
                for(let clz of classList)
                    element.classList.add(clz);
            }
            return element;
        },
        generateTOC: function(sections) {
            let navElement = document.createElement("ul");
            let level1Counter = 0;
            for(let section of sections) {
                level1Counter ++;

                let itemElement = document.createElement("li");
                let h1Element = section.querySelector("h1");
                this.convertTitleToLink(null, {
                    titleElement: h1Element,
                    liElement: itemElement
                });
                this.createRomanCounterElement([level1Counter], {
                    target: h1Element
                })

                navElement.appendChild(itemElement); {
                    let subtitles = section.querySelectorAll("h2");
                    if(subtitles.length == 0)
                        continue;
                    let subNavElement = document.createElement("ul");

                    let level2Counter = 0;
                    for(let h2Element of subtitles) {
                        level2Counter ++;

                        let itemElement = document.createElement("li");
                        this.convertTitleToLink(null, {
                            titleElement: h2Element,
                            liElement: itemElement
                        });
                        this.createRomanCounterElement([level1Counter, level2Counter], {
                            target: h2Element,
                            classList: ["NavigationMap_romanCounter"]
                        })
                        subNavElement.appendChild(itemElement);
                    }
                    itemElement.appendChild(subNavElement);
                }
            }
            return navElement;
        }
    };

    return NavigationMap;

})();