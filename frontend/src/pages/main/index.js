import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import styles from './styles.module.css'
import { useRecipes } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const HomePage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipes,
    recipesCount,
    setRecipesCount,
    recipesPage,
    setRecipesPage,
    tagsValue,
    setTagsValue,
    is_staff,
    handleTagsChange,
    handleLike,
    handleAddToCart,
  } = useRecipes()


  const getRecipes = ({ page = 1, rubric }) => {
    api
      .getRecipes({ page, rubric })
      .then(res => {
        const { results, count } = res
        setRecipes(results)
        setRecipesCount(count)
      })
  }

  useEffect(_ => {
    getRecipes({ page: recipesPage, rubric: tagsValue })
  }, [recipesPage, tagsValue])

  useEffect(_ => {
    api.getTags()
      .then(rubric => {
        setTagsValue(rubric.map(rubric => ({ ...rubric, value: true })))
      })
  }, [])


  return <Main>
    <Container>
      <MetaTags>
        <title>Курсы</title>
        <meta name="description" content="Кружки - направления" />
        <meta property="og:title" content="Кружки" />
      </MetaTags>
      <div className={styles.title}>
        <Title title='Направления' />
        <CheckboxGroup
          values={tagsValue}
          handleChange={value => {
            setRecipesPage(1)
            handleTagsChange(value)
          }}
        />
      </div>
      <CardList>
        {recipes.map(card => <Card
          {...card}
          key={card.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>
      <dev>
      { authContext && is_staff && <Button
              className={styles['single-card__button']}
              modifier='style_light-blue'
              href='groups/create'
            >
              'Добавить новую группу'
            </Button>}
      </dev>
      <Pagination
        count={recipesCount}
        limit={6}
        page={recipesPage}
        onPageChange={page => setRecipesPage(page)}
      />
    </Container>
  </Main>
}

export default HomePage

