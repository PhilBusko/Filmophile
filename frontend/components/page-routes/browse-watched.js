/**************************************************************************************************
BROWSE WATCHED MOVIES PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
//import { When } from 'react-if';

import MenuLayout from '../layouts/menu-layout'
import SelectWrapper from '../elements/select-wrapper'
import Paginator, { PERPAGE } from '../elements/paginator'
import MoviesPanel from '../elements/movies-panel'

class BrowseWatched extends React.Component {

    state = {
        genres: [],
        movies: [],
        offset: 0,
        filters: {}
    }

    componentDidMount() {
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
            url: 'api/movies/movies_watched/',
            method: 'get',
        }).then( success => {
            this.setState({
                movies: success.data,
            });
        }).catch( error => {
            console.log('Axios Error: api/movies/movies_watched/')
            console.log(error);
        });
    }

    updateCurrentPage = (newOffset) => {
        this.setState({offset: newOffset});
    }

    getTrimmedMovies = () => {
        let filtered = this.state.movies.filter( m => m);
        let paginated = filtered.slice(this.state.offset, this.state.offset + PERPAGE)
        return paginated;
    }

    excludeGenre = () => {
    }

    includeGenre = () => {
    }

    render() {
        return (
            <MenuLayout>
                <div className='pure-g sticky-grid spacing-outer'>
                    <div className='pure-u-lg-6-24'>
                        <div className='page-title spacing-inner'>
                            Watched Movies
                        </div>
                    </div>

                    <div className='pure-u-lg-10-24'>
                        <div className='control-group spacing-inner'>
                            <div className='left-panel control-outer'>
                                <div className='control-inner'>
                                    <SelectWrapper 
                                        options={ ['None'].concat(this.state.genres) } 
                                        label={ 'Exclude Genre' } 
                                        updateSelection={ this.excludeGenre }
                                    />
                                </div>
                                <div className='control-inner'>
                                    <SelectWrapper 
                                        options={ ['All'].concat(this.state.genres) } 
                                        label={ 'Include Genre' } 
                                        updateSelection={ this.includeGenre }
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className='pure-u-lg-8-24'>
                        <div className='control-group spacing-inner'>
                            <Paginator 
                                numberEntries={ this.state.movies.length } 
                                updateCurrentPage={ this.updateCurrentPage }
                            />
                        </div>
                    </div>
                </div>

                <MoviesPanel movies={ this.getTrimmedMovies() }></MoviesPanel>

            </MenuLayout>
        );
    }
}

export default BrowseWatched;
