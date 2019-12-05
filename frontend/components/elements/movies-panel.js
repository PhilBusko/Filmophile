/**************************************************************************************************
MOVIES PANEL ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import { When } from 'react-if';

import MovieCard from '../elements/movie-card'
import './movies-panel.scss'

class MoviesPanel extends React.Component {

    loadingIcon = require('../assets/controls/loading_cat.gif')

    static propTypes = {
        movies: PropTypes.array.isRequired,
    }

    render() {
        return (
            <div className='movies-wrapper'>
                <div className='pure-g movie-outer'>
                    <When condition={ this.props.movies.length > 0 }>
                        {this.props.movies.map((mov, idx) => (
                            <div key={ idx } className='pure-u-8-24 pure-u-xxl-6-24 pure-u-xxxl-1-5'>
                                <div className='movie-inner'>
                                    <MovieCard movie={ mov } />
                                </div>
                            </div>
                        ))}
                    </When>
                    <When condition={ this.props.movies.length == 0 }>
                        <div style={{ width: '100%', height: '700px'}} className='center-both'>
                            <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                        </div>
                    </When>
                </div>
            </div>
        );
    }
}

export default MoviesPanel;
