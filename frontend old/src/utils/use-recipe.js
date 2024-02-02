import React, { useState } from "react";
import api from '../api'

export default function useGroup () {
  const [ Group, setGroup ] = useState({})

  const handleLike = ({ id, toLike = 1 }) => {
    const method = toLike ? api.addToFavorites.bind(api) : api.removeFromFavorites.bind(api)
    method({ id }).then(res => {
      const GroupUpdated = { ...Group, is_favorited: Number(toLike) }
      setGroup(GroupUpdated)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  const handleAddToCart = ({ id, toAdd = 1, callback }) => {
    const method = toAdd ? api.addToOrders.bind(api) : api.removeFromOrders.bind(api)
    method({ id }).then(res => {
      const GroupUpdated = { ...Group, is_in_shopping_cart: Number(toAdd) }
      setGroup(GroupUpdated)
      callback && callback(toAdd)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  const handleSubscribe = ({ author_id, toSubscribe = 1 }) => {
    const method = toSubscribe ? api.subscribe.bind(api) : api.deleteSubscriptions.bind(api)
      method({
        author_id
      })
      .then(_ => {
        const GroupUpdated = { ...Group, author: { ...Group.author, is_subscribed: toSubscribe } }
        setGroup(GroupUpdated)
      })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  return {
    Group,
    setGroup,
    handleLike,
    handleAddToCart,
    handleSubscribe
  }
}
