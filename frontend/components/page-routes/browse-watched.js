/**************************************************************************************************
RULES-LOADER PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import { When } from 'react-if';

import MenuLayout from '../layouts/menu-layout'
import './browse-watched.scss'

class BrowseWatched extends React.Component {

    state = {
        watchedMovies: null,
    }

    componentDidMount() {
        axios({
            url: 'api/movies/movies_watched/',
            method: 'get',
            data: { }
        }).then( success => {
            console.log(success.data)
            var updateState = {watchedMovies: success.data};
            this.setState({...this.state, ...updateState});
        }).catch( error => {
            console.log('Axios Error: api/movies/movies_watched/')
            console.log(error);
        });
    }

    render() {
        return (
            <MenuLayout>
                <div className='pure-g'>

                    <div className='pure-u-1 page-title grid-spacing'>
                        Browse Watched Movies
                    </div>
                    
                    <div className='pure-u-1 grid-spacing'>
                        <When condition={ !!this.state.watchedMovies }>
                        { () =>
                            <div className='movie-panel'>
                                { this.state.watchedMovies.length }
                            </div>
                        }
                        </When>
                        <When condition={ !this.state.watchedMovies }>
                        { () =>
                            <div>movies loading ...</div>
                        }
                        </When>
                    </div>

                </div>
            </MenuLayout>
        );
    }
}

export default BrowseWatched;
