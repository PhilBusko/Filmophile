/**************************************************************************************************
ABOUT PAGE
**************************************************************************************************/
import React, { Component } from 'react';
import MenuLayout from '../layouts/menu-layout'
import { ResourceLink } from '../elements'

class About extends Component {

    moviedbIcon = require('../assets/icons/moviedb.svg')
    reelgoodIcon = require('../assets/icons/reelgood.png')
    imdbIcon = require('../assets/icons/imdb.ico')
    jupyterIcon = require('../assets/icons/jupyter.png')
    pandasIcon = require('../assets/icons/pandas.png')
    seleniumIcon = require('../assets/icons/selenium.ico')
    sklearnIcon = require('../assets/icons/sklearn.ico')
    xgboostIcon = require('../assets/icons/xgboost.png')
    plotlyIcon = require('../assets/icons/plotly.png')
    djangoIcon = require('../assets/icons/django.png')
    postgresIcon = require('../assets/icons/postgres.png')
    reactIcon = require('../assets/icons/react.ico')
    sassIcon = require('../assets/icons/sass.png')
    purecssIcon = require('../assets/icons/purecss.png')
    webpackIcon = require('../assets/icons/webpack.ico')
    githubIcon = require('../assets/icons/github.png')

    render() {
        return (
            <MenuLayout>
                <div className='pure-g spacing-outer'>

                    <div className='pure-u-1'>
                        <div className='spacing-inner page-title'>
                            About Phil-mo-phile
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner'>
                            This site aggregates movies and TV shows from different streaming services
                            and makes them all available in one place. 
                            The user votes on their favorite and disliked movies, 
                            and the computer model learns their preferences from that information. 
                            The model then makes recommendations for new movies in three types: Love It, Maybe, and Don't Bother.
                            The site was first built for the&nbsp;
                            <a className='link-format' href='https://flatironschool.com/' target='blank_'
                                style={{'display': 'contents'}}>FlatIron School's</a>
                            &nbsp;Data Science Bootcamp,
                            but it is a dear project, and has been expanded since.
                            It combines three of my pasions: data science, web development, and movies.
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner'>
                            <span className='entry-title'>Recommendation System: </span> 
                            Though the site features a recommendation engine for movies,
                            it is not the same as the classic&nbsp;
                            <a className='link-format' href='https://en.wikipedia.org/wiki/Recommender_system' target='blank_'>recommender system</a>
                            &nbsp;as found on Netflix, Amazon, Ebay, etc.
                            The classic system requires knowledge of hundreds of users, as well as hundreds of products they bought/viewed.
                            It then uses matrix multiplication to draw inferences about other products 
                            the users may be interested in. 
                            This system is ubiquitous because it doesn't require the user to score anything,
                            the inferences are drawn based on the user's behavior on the site.
                            <br></br>
                            &nbsp;&nbsp;&nbsp;&nbsp;The goal of this site is to have a much more precise measure 
                            of how a user prefers their movies. 
                            So instead, a classification algorithm is used.
                            The model is trained on all movies that the user has scored.
                            The algorithm then makes recommendations for all the movies the user hasn't seen yet.
                            It's my belief that this produces better recommendations than the classic engine.
                            Though it may be more precise, 
                            it also comes with the cost of forcing the user to score hundreds of movies 
                            before they can get very good recommendations.
                       </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner'>
                            <span className='entry-title'>Webmaster: </span> 
                            <a href='https://www.linkedin.com/in/phillipbusko' className='link-format' target='blank_'>Phillip Busko</a>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner'>
                            <span className='entry-title'>Presentation: </span>
                            <a href='https://docs.google.com/presentation/d/1aqI7jCI6Vg6Tp6t-_Gk7SuNp51bvD_885ZGPFv6b-ZY/edit?usp=sharing'
                                className='link-format' target='blank_'>Google Slides</a>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            Resource & Package Credits
                        </div>
                    </div>
                    <div className='pure-u-1 '>
                        <div className='spacing-inner left-panel'>
                            <span className='entry-title'>Data Sources:</span> 
                            <span>
                                <ResourceLink url={'https://www.themoviedb.org'} 
                                    icon={ this.moviedbIcon } text='TMDB'></ResourceLink>
                                <ResourceLink url={'https://reelgood.com/'} 
                                    icon={ this.reelgoodIcon } text='Reelgood'></ResourceLink>
                                <ResourceLink url={'https://www.imdb.com/'} 
                                    icon={ this.imdbIcon } text='IMDB' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                        <div className='spacing-inner left-panel'>
                            <span className='entry-title'>Data Science:</span> 
                            <span>
                                <ResourceLink url={'https://jupyter.org/'} 
                                    icon={ this.jupyterIcon } text='Jupyter Project'></ResourceLink>
                                <ResourceLink url={'https://pandas.pydata.org/'} 
                                    icon={ this.pandasIcon } text='pandas'></ResourceLink>
                                <ResourceLink url={'https://selenium.dev/'} 
                                    icon={ this.seleniumIcon } text='Selenium'></ResourceLink>
                                <ResourceLink url={'https://scikit-learn.org/stable/'} 
                                    icon={ this.sklearnIcon } text='scikit-learn'></ResourceLink>
                                <ResourceLink url={'https://xgboost.readthedocs.io/en/latest/index.html#'} 
                                    icon={ this.xgboostIcon } text='XGBoost'></ResourceLink>
                                <ResourceLink url={'https://plot.ly/python/'} 
                                    icon={ this.plotlyIcon } text='plot.ly' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                        <div className='spacing-inner left-panel'>
                            <span className='entry-title'>Backend:</span> 
                            <span>
                                <ResourceLink url={'https://www.djangoproject.com/'} 
                                    icon={ this.djangoIcon } text='Django'></ResourceLink>
                                <ResourceLink url={'https://www.postgresql.org/'} 
                                    icon={ this.postgresIcon } text='PostgreSQL' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                        <div className='spacing-inner left-panel'>
                            <span className='entry-title'>Frontend:</span> 
                            <span>
                                <ResourceLink url={'https://reactjs.org/'} 
                                    icon={ this.reactIcon } text='React'></ResourceLink>
                                <ResourceLink url={'https://sass-lang.com/'} 
                                    icon={ this.sassIcon } text='Sass'></ResourceLink>
                                <ResourceLink url={'https://purecss.io/'} 
                                    icon={ this.purecssIcon } text='Pure.css'></ResourceLink>
                                <ResourceLink url={'https://webpack.js.org/'} 
                                    icon={ this.webpackIcon } text='webpack' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                        <div className='spacing-inner left-panel'>
                            <span className='entry-title'>Deployment:</span> 
                            <span>
                                <ResourceLink url={'https://github.com/PhilBusko/Filmophile'} 
                                    icon={ this.githubIcon } text='Github Repo'></ResourceLink>
                                <ResourceLink url={'https://github.com/PhilBusko/Filmophile'} 
                                    icon={ this.githubIcon } text='PaaS' isLast={ true }></ResourceLink>
                            </span>
                        </div>
                    </div>

                </div>
            </MenuLayout>
        ); }
    }

export default About;
