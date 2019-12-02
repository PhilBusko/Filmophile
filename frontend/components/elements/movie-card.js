/**************************************************************************************************
MOVIE CARD ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import './movie-card.scss'

class MovieCard extends React.Component {

    static propTypes = {
        movie: PropTypes.object.isRequired,
    }

    render() {
        let movie = this.props.movie;
        let indecesRaw = JSON.parse(movie['Indeces']);
        let indeces = [];
        let imdbHref = 'https://www.imdb.com/title/';

        for (var key in indecesRaw) {
            let service = null;
            if (key === 'netflix') {
                service = {
                    'href': `https://www.netflix.com/title/${indecesRaw[key]}`,
                    'text': 'Netflix',
                }
            }
            if (key === 'amazon') {
                service = {
                    'href': `https://www.amazon.com/gp/video/detail/${indecesRaw[key]}`,
                    'text': 'Amazon',
                }
            }
            if (key === 'hulu') {
                service = {
                    'href': `https://www.hulu.com/movie/${indecesRaw[key]}`,
                    'text': 'Hulu',
                }
            }            
            if (key === 'imdb') {
                imdbHref += indecesRaw[key]
            }

            if (service) 
                indeces.push(service);
        }

        return (
            <div className='movie-card movie-panel'>
                <div className='poster-spacer'>
                    <img className='poster-format' src={ movie['Poster'] } alt=''></img>
                </div>
                <div className='info-panel'>
                    <div>
                        <span className='strong-font'>{ movie['Title'] }</span>  
                        <span className='small-font'> ({ movie['Year'] })</span>
                    </div>
                    <div className='spaced-panel'>
                        <span className='small-font'>
                            <a href={ imdbHref } className='imdb-link' target='blank_'>IMDB</a>
                            <span>: { movie['ScoreImdb'].toFixed(1) }</span>
                        </span>
                        <span>stars</span>
                    </div>
                    <div>
                        <span className='small-font'>{ movie['Genres'] }</span>
                    </div>
                    <div className='even-panel'>
                        { indeces.map((srv, idx) => (
                            <div key={ idx }>
                                <a className='service-link' href={ srv['href'] } target='blank_'>{ srv['text'] }</a>
                            </div>
                        ))}
                    </div>
               </div>
            </div>
        );
    }
}

export default MovieCard;
