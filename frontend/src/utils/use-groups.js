import React, { useState } from "react";
import { useTags } from './index.js'
import api from '../api/index.js'

export default function useGroups () {
  const [ Groups, setGroups ] = useState([])
  const [ GroupsCount, setGroupsCount ] = useState(0)
  const [ GroupsPage, setGroupsPage ] = useState(1)
  const { value: tagsValue, handleChange: handleTagsChange, setValue: setTagsValue } = useTags()

  const handleLike = ({ id, toLike = true }) => {
    const method = toLike ? api.addToFavorites.bind(api) : api.removeFromFavorites.bind(api)
    method({ id }).then(res => {
      const GroupsUpdated = Groups.map(Group => {
        if (Group.id === id) {
          Group.is_favorited = toLike
        }
        return Group
      })
      setGroups(GroupsUpdated)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  const handleAddToCart = ({ id, toAdd = true, callback }) => {
    const method = toAdd ? api.addToOrders.bind(api) : api.removeFromOrders.bind(api)
    method({ id }).then(res => {
      const GroupsUpdated = Groups.map(Group => {
        if (Group.id === id) {
          Group.is_in_shopping_cart = toAdd
        }
        return Group
      })
      setGroups(GroupsUpdated)
      callback && callback(toAdd)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  return {
    Groups,
    setGroups,
    GroupsCount,
    setGroupsCount,
    GroupsPage,
    setGroupsPage,
    tagsValue,
    handleLike,
    handleAddToCart,
    handleTagsChange,
    setTagsValue
  }
}
