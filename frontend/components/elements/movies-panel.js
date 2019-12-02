/**************************************************************************************************
MOVIES PANEL ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';

import MovieCard from '../elements/movie-card'
import './movies-panel.scss'

class MoviesPanel extends React.Component {

    static propTypes = {
        movies: PropTypes.array.isRequired,
    }

    render() {
        return (
            <div className='movies-wrapper'>
                <div className='pure-g movie-outer'>
                    {this.props.movies.map((mov, idx) => (
                        <div key={ idx } className='pure-u-lg-8-24 pure-u-xxl-6-24 pure-u-xxxl-1-5'>
                            <div className='movie-inner'>
                                <MovieCard movie={ mov } />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }
}

export default MoviesPanel;
