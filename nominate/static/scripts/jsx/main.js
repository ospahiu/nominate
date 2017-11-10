var DynamicSearch = React.createClass({

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
            <div>
                <input
                    type="text"
                    value={this.state.searchString}
                    onChange={this.handleChange}
                    placeholder="i.e. The God Father"/>
                <ul>
                    {movies.map(function (movie) {
                        return <li>{[movie.title + " " + movie.year]} </li>
                    })}
                </ul>
            </div>
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
    <DynamicSearch movies={JSON.parse(movies)}/>,
    document.getElementById('main')
);
