/**************************************************************************************************
BROWSE WATCHED MOVIES PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import MenuLayout from '../layouts/menu-layout'
import { SelectWrapper, Paginator, PERPAGE, MoviesPanel, TextWrapper } from '../elements'

class BrowseWatched extends React.Component {

    state = {
        genres: [],
        movies: [],
        offset: 0,
        filters: {}
    }

    componentDidMount() {
        axios({
            url: 'api/recommend/genres/',
        }).then( success => {
            this.setState({ genres: success.data });
        }).catch( error => {
            console.log('Axios Error: api/recommend/genres/')
            console.log(error);
        });

        axios({
            url: 'api/recommend/movies_watched/',
        }).then( success => {
            this.setState({ movies: success.data });
        }).catch( error => {
            console.log('Axios Error: api/recommend/movies_watched/')
            console.log(error);
        });
    }

    getPaginatedMovies = (filtered) => {
        let paginated = filtered.slice(this.state.offset, this.state.offset + PERPAGE)
        return paginated;
    }

    getFilteredMovies = () => {
        let filters = this.state.filters;
        let filterMovies = this.state.movies;

        for (var key in filters) {

            if (key === 'excludeGenre') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => (mv['Genres'] ? mv['Genres'] : '').indexOf(filters[key]) === -1 );

            if (key === 'includeGenre') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => (mv['Genres'] ? mv['Genres'] : '').indexOf(filters[key]) !== -1 );

            if (key === 'filterTitle') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => mv['Title'].toLowerCase().indexOf(filters[key].toLowerCase()) >= 0 );
        }

        return filterMovies;
    }

    updateOffset = (newOffset) => {
        this.setState({offset: newOffset});
    }

    excludeGenre = (newValue) => {
        let intValue = parseInt(newValue);
        let newFilters = this.state.filters;
        if (intValue != 0)
            newFilters['excludeGenre'] = this.state.genres.filter(g => g['key'] === intValue)[0]['value'];
        else
            delete newFilters['excludeGenre']
        this.setState({filters: newFilters});
    }

    includeGenre = (newValue) => {
        let intValue = parseInt(newValue);
        let newFilters = this.state.filters;
        if (intValue != 0)
            newFilters['includeGenre'] = this.state.genres.filter(g => g['key'] === intValue)[0]['value'];
        else
            delete newFilters['includeGenre']
        this.setState({filters: newFilters});
    }

    filterTitle = (newText) => {
        let strValue = newText.toString();
        let newFilters = this.state.filters;
        if (strValue.length >= 3)
            newFilters['filterTitle'] = strValue;
        else
            delete newFilters['filterTitle']
        this.setState({ 
            filters: newFilters,
            offset: 0, 
        });
    }

    render() {

        let filteredMovies = this.getFilteredMovies();
        let paginatedMovies = this.getPaginatedMovies(filteredMovies);

        return (
            <MenuLayout>
                <div className='left-panel spacing-outer sticky-top'>

                    <div> 
                        <div className='spacing-inner'>
                            <div className='page-title'>
                                Watched Movies
                            </div>
                        </div>
                        <div className='spacing-inner control-island control-outer'>
                            <div className='control -inner'>
                                <Paginator 
                                    numberEntries={ filteredMovies.length } 
                                    updateCurrentPage={ this.updateOffset }
                                />
                            </div>
                        </div>
                    </div>

                    <div className='spacing-inner control-island control-outer'>
                        <div className='control-inner'>
                            <TextWrapper 
                                label={ 'Search' } 
                                updateText={ this.filterTitle }
                            />
                        </div>
                        <div className='panel-new-line'></div>
                        <div className='control-inner'>
                            <SelectWrapper 
                                options={ [{'key': 0, 'value': 'None'}].concat(this.state.genres) } 
                                label={ 'Exclude Genre' } 
                                updateSelection={ this.excludeGenre }
                            />
                        </div>
                        <div className='control-inner'>
                            <SelectWrapper 
                                options={ [{'key': 0, 'value': 'All'}].concat(this.state.genres) } 
                                label={ 'Include Genre' } 
                                updateSelection={ this.includeGenre }
                            />
                        </div>
                    </div>

                </div>

                <MoviesPanel movies={ paginatedMovies }></MoviesPanel>

            </MenuLayout>
        );
    }
}

export default BrowseWatched;
