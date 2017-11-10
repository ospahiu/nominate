(function e(t, n, r) {
    function s(o, u) {
        if (!n[o]) {
            if (!t[o]) {
                var a = typeof require == "function" && require;
                if (!u && a) return a(o, !0);
                if (i) return i(o, !0);
                var f = new Error("Cannot find module '" + o + "'");
                throw f.code = "MODULE_NOT_FOUND", f
            }
            var l = n[o] = {exports: {}};
            t[o][0].call(l.exports, function (e) {
                var n = t[o][1][e];
                return s(n ? n : e)
            }, l, l.exports, e, t, n, r)
        }
        return n[o].exports
    }

    var i = typeof require == "function" && require;
    for (var o = 0; o < r.length; o++) s(r[o]);
    return s
})({
    1: [function (require, module, exports) {
        var DynamicSearch = React.createClass({
            displayName: "DynamicSearch",

            // sets initial state
            getInitialState: function () {
                return {searchString: ''};
            },

            // sets state, triggers render method
            handleChange: function (event) {
                // grab value form input box
                this.setState({searchString: event.target.value});
                console.log("scope updated!");
            },

            render: function () {

                var movies = this.props.movies;
                var searchString = this.state.searchString.trim().toLowerCase();

                // filter countries list by value from input box
                if (searchString.length > 0) {
                    movies = movies.filter(function (movie) {
                        return movie.title.toLowerCase().match(searchString);
                    });
                }

                console.error(movies);

                return (
                    React.createElement("div", null,
                        React.createElement("input", {
                            type: "text",
                            value: this.state.searchString,
                            onChange: this.handleChange,
                            placeholder: "i.e. The God Father"
                        }),
                        React.createElement("ul", null,
                            movies.map(function (movie) {
                                return React.createElement("li", null, [movie.title + " " + movie.year], " ")
                            })
                        )
                    )
                )
            }

        });

// list of countries, defined with JavaScript object literals
// var countries = [
//     {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
//     {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
//     {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
//     {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
//     {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
//     {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
//     {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
// ];

// var movies = '{{ movies }}';


// fetch('/movies')
//   .then((res)=>{ console.error(res)});

        ReactDOM.render(
            React.createElement(DynamicSearch, {movies: JSON.parse(movies)}),
            document.getElementById('main')
        );

    }, {}]
}, {}, [1]);
