import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import styles from './styles.module.css'
import { useGroups } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const HomePage = ({ updateOrders }) => {
  const {
    Groups,
    setGroups,
    GroupsCount,
    setGroupsCount,
    GroupsPage,
    setGroupsPage,
    tagsValue,
    setTagsValue,
    handleTagsChange,
    handleLike,
    handleAddToCart
  } = useGroups()


  const getGroups = ({ page = 1, tags }) => {
    api
      .getGroups({ page, tags })
      .then(res => {
        const { results, count } = res
        setGroups(results)
        setGroupsCount(count)
      })
  }

  useEffect(_ => {
    getGroups({ page: GroupsPage, tags: tagsValue })
  }, [GroupsPage, tagsValue])

  useEffect(_ => {
    api.getTags()
      .then(tags => {
        setTagsValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])


  return <Main>
    <Container>
      <MetaTags>
        <title>Рецепты</title>
        <meta name="description" content="Продуктовый помощник - Рецепты" />
        <meta property="og:title" content="Рецепты" />
      </MetaTags>
      <div className={styles.title}>
        <Title title='Рецепты' />
        <CheckboxGroup
          values={tagsValue}
          handleChange={value => {
            setGroupsPage(1)
            handleTagsChange(value)
          }}
        />
      </div>
      <CardList>
        {Groups.map(card => <Card
          {...card}
          key={card.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>
      <Pagination
        count={GroupsCount}
        limit={6}
        page={GroupsPage}
        onPageChange={page => setGroupsPage(page)}
      />
    </Container>
  </Main>
}

export default HomePage

