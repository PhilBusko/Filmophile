/**************************************************************************************************
BROWSE TO-WATCH MOVIES PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
//import { When } from 'react-if';

import MenuLayout from '../layouts/menu-layout'
import SelectWrapper from '../elements/select-wrapper'
import Paginator, { PERPAGE } from '../elements/paginator'
import MoviesPanel from '../elements/movies-panel'

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

    getTrimmedMovies = () => {
        let filtered = this.getFilteredMovies();
        //console.log('filtered result: ' +filtered.length)
        let paginated = filtered.slice(this.state.offset, this.state.offset + PERPAGE)
        return paginated;
    }

    getFilteredMovies = () => {
        let filters = this.state.filters;
        let filterMovies = this.state.movies;

        for (var key in filters) {

            //console.log(key + ' : ' + filters[key]);

            if (key === 'recomLevel') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => mv['RecomLevel'] === filters[key] );

            if (key === 'excludeGenre' && filters[key] !== 'None') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => (mv['Genres'] ? mv['Genres'] : '').indexOf(filters[key]) === -1 );

            if (key === 'includeGenre' && filters[key] !== 'All') 
                // eslint-disable-next-line
                filterMovies = filterMovies.filter( mv => (mv['Genres'] ? mv['Genres'] : '').indexOf(filters[key]) !== -1 );
        }

        return filterMovies;
    }

    updateOffset = (newOffset) => {
        this.setState({offset: newOffset});
    }

    changeRecommendation = (newValue) => {
        let filters = this.state.filters;
        filters['recomLevel'] = newValue;
        this.setState({filters: filters});
    }

    excludeGenre = (newValue) => {
        let filters = this.state.filters;
        filters['excludeGenre'] = this.state.genres.filter(g => g['key'] === newValue)[0]['value'];
        this.setState({filters:filters});
    }

    includeGenre = (newValue) => {
        let filters = this.state.filters;
        filters['includeGenre'] = this.state.genres.filter(g => g['key'] === newValue)[0]['value'];
        this.setState({filters: filters});
    }

    render() {
        return (
            <MenuLayout>
                <div className='spacing-outer sticky-top control-panel'>

                    <div className='spacing-inner page-title'>
                        To Watch Movies
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
                            numberEntries={ this.getFilteredMovies().length } 
                            updateCurrentPage={ this.updateOffset }
                        />
                    </div>

                </div>                     

                <MoviesPanel movies={ this.getTrimmedMovies() }></MoviesPanel>

            </MenuLayout>
        );
    }
}

export default BrowseToWatch;
