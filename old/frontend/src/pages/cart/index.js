import { PurchaseList, Title, Container, Main, Button } from '../../components'
import styles from './styles.module.css'
import { useGroups } from '../../utils/index.js'
import { useEffect, useState } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const Cart = ({ updateOrders, orders }) => {
  const {
    groups,
    setGroups,
    handleAddToCart
  } = useGroups()
  
  const getGroups = () => {
    api
      .getGroups({
        page: 1,
        limit: 999,
        //is_in_shopping_cart: Number(true)
      })
      .then(res => {
        const { results } = res
        setGroups(results)
      })
  }

  useEffect(_ => {
    getGroups()
  }, [])

  const downloadDocument = () => {
    api.downloadFile()
  }

  return <Main>
    <Container className={styles.container}>
      <MetaTags>
        <title>Список покупок</title>
        <meta name="description" content="Продуктовый помощник - Список покупок" />
        <meta property="og:title" content="Список покупок" />
      </MetaTags>
      <div className={styles.cart}>
        <Title title='Список покупок' />
        <PurchaseList
          orders={Groups}
          handleRemoveFromCart={handleAddToCart}
          updateOrders={updateOrders}
        />
        {orders > 0 && <Button
          modifier='style_dark-blue'
          clickHandler={downloadDocument}
        >Скачать список</Button>}
      </div>
    </Container>
  </Main>
}

export default Cart
