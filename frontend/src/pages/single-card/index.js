import { Container, Main, Button, TagsContainer, Icons, LinkComponent } from '../../components'
import { UserContext, AuthContext } from '../../contexts'
import { useContext, useState, useEffect } from 'react'
import styles from './styles.module.css'
import Ingredients from './ingredients'
import Description from './description'
import cn from 'classnames'
import { useRouteMatch, useParams, useHistory } from 'react-router-dom'
import MetaTags from 'react-meta-tags'

import { useRecipe } from '../../utils/index.js'
import api from '../../api'

const SingleCard = ({ loadItem, updateOrders }) => {
  const [ loading, setLoading ] = useState(true)
  const {
    recipe,
    setRecipe,
    handleLike,
    handleAddToCart,
    handleSubscribe
  } = useRecipe()
  const authContext = useContext(AuthContext)
  const userContext = useContext(UserContext)
  const { id } = useParams()
  const history = useHistory()

  useEffect(_ => {
    api.getRecipe ({
        recipe_id: id
      })
      .then(res => {
        setRecipe(res)
        setLoading(false)
      })
      .catch(err => {
        history.push('/groups')
      })
  }, [])
  
  const { url } = useRouteMatch()
  const {
    teacher = {},
    image,
    rubric,
    number_of_lessons,
    name,
    ingredients,
    description,
    is_joining,
    is_in_shopping_cart
  } = recipe
  
  return <Main>
    <Container>
      <MetaTags>
        <title>{name}</title>
        <meta name="description" content={`Продуктовый помощник - ${name}`} />
        <meta property="og:title" content={name} />
      </MetaTags>
      <div className={styles['single-card']}>
        <img src={image} alt={name} className={styles["single-card__image"]} />
        <div className={styles["single-card__info"]}>
          <div className={styles["single-card__header-info"]}>
              <h1 className={styles["single-card__title"]}>{name}</h1>
              {authContext && <Button
                modifier='style_none'
                clickHandler={_ => {
                  handleLike({ id, toLike: Number(!is_joining) })
                }}
              >
                {is_joining ? <Icons.StarBigActiveIcon /> : <Icons.StarBigIcon />}
              </Button>}
          </div>
          <TagsContainer tags={rubric} />
          <div>
            <p className={styles['single-card__text']}><Icons.ClockIcon /> {number_of_lessons} ч.</p>
            <p className={styles['single-card__text_with_link']}>
              <div className={styles['single-card__text']}>
                <Icons.UserIcon /> <LinkComponent
                  title={`${teacher.first_name} ${teacher.last_name}`}
                  href={`/user/${teacher.id}`}
                  className={styles['single-card__link']}
                />
              </div>
              {(userContext || {}).id === teacher.id && <LinkComponent
                href={`${url}/edit`}
                title='Редактировать рецепт'
                className={styles['single-card__edit']}
              />}
            </p>
          </div>
          <div className={styles['single-card__buttons']}>
            {authContext && <Button
              className={styles['single-card__button']}
              modifier={is_joining ? 'style_light' : 'style_dark-blue'}
              clickHandler={_ => {
                handleAddToCart({ id, toAdd: Number(!is_joining), callback: updateOrders })
              }}
            >
              
            {is_joining ? <><Icons.DoneIcon color="#4A61DD"/>Заявка подана</> : <><Icons.PlusIcon /> Подать заявку</>}
            </Button>}
            {(userContext || {}).id !== teacher.id && authContext && <Button
              className={styles['single-card__button']}
              modifier='style_light-blue'
              clickHandler={_ => {
                handleSubscribe({ teacher_id: teacher.id, toSubscribe: !teacher.is_subscribed })
              }}
            >
              {teacher.is_subscribed ? 'Отписаться от автора' : 'Подписаться на автора'}
            </Button>}
          </div>
          <Ingredients ingredients={ingredients} />
          <Description description={description} />
        </div>
    </div>
    </Container>
  </Main>
}

export default SingleCard

