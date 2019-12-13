/**************************************************************************************************
BROWSE TO-WATCH MOVIES PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
//import { When } from 'react-if';

import MenuLayout from '../layouts/menu-layout'
import { SelectWrapper, Paginator, PERPAGE, MoviesPanel } from '../elements'

class BrowseToWatch extends React.Component {

    state = {
        recomLevels: [],
        genres: [],
        movies: [],
        offset: 0,
        filters: { 'recomLevel': 3 },
    }

    componentDidMount() {
        axios({
            url: 'api/movies/recom_levels/',
            method: 'get',
        }).then( success => {
            this.setState({
                recomLevels: success.data,
            });
        }).catch( error => {
            console.log('Axios Error: api/movies/recom_levels/')
            console.log(error);
        });

        axios({
            url: 'api/movies/genres/',
            method: 'get',
        }).then( success => {
            this.setState({
                genres: success.data,
            });
        }).catch( error => {
            console.log('Axios Error: api/movies/genres/')
            console.log(error);
        });

        axios({
            url: 'api/movies/movies_towatch/',
            method: 'get',
        }).then( success => {
            this.setState({
                movies: success.data,
            });
        }).catch( error => {
            console.log('Axios Error: api/movies/movies_towatch/')
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

            //console.log(key + ' : ' + filters[key]);

            if (key === 'recomLevel') {
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => mv['RecomLevel'] === filters[key] );
            }

            if (key === 'excludeGenre') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => (mv['Genres'] ? mv['Genres'] : '').indexOf(filters[key]) === -1 );

            if (key === 'includeGenre') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => (mv['Genres'] ? mv['Genres'] : '').indexOf(filters[key]) !== -1 );
        }

        return filterMovies;
    }

    updateOffset = (newOffset) => {
        this.setState({offset: newOffset});
    }

    changeRecommendation = (newValue) => {
        let intValue = parseInt(newValue);
        let filters = this.state.filters;
        filters['recomLevel'] = intValue;
        this.setState({filters: filters});
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

    render() {

        let filteredMovies = this.getFilteredMovies();
        let paginatedMovies = this.getPaginatedMovies(filteredMovies);

        return (
            <MenuLayout>
                <div className='spacing-outer sticky-top control-panel'>

                    <div className='spacing-inner page-title'>
                        Recommended Movies
                    </div>

                    <div className='spacing-inner control-group control-filter'>
                        <div className='left-panel control-outer'>
                            <div className='control-inner'>
                                <SelectWrapper 
                                    options={ this.state.recomLevels } 
                                    label={ 'Recommendation Type' } 
                                    updateSelection={ this.changeRecommendation }
                                />
                            </div>
                            <div className='control-dummy'>
                            </div>
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

                    <div className='spacing-inner control-group control-paginator'>
                        <Paginator 
                            numberEntries={ filteredMovies.length } 
                            updateCurrentPage={ this.updateOffset }
                        />
                    </div>

                </div>                     

                <MoviesPanel movies={ paginatedMovies }></MoviesPanel>

            </MenuLayout>
        );
    }
}

export default BrowseToWatch;
