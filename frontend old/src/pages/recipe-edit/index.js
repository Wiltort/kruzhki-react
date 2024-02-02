import { Container, IngredientsSearch, FileInput, Input, Title, CheckboxGroup, Main, Form, Button, Checkbox, Textarea } from '../../components'
import styles from './styles.module.css'
import api from '../../api'
import { useEffect, useState } from 'react'
import { useTags } from '../../utils'
import { useParams, useHistory } from 'react-router-dom'
import MetaTags from 'react-meta-tags'

const GroupEdit = ({ onItemDelete }) => {
  const { value, handleChange, setValue } = useTags()
  const [ GroupName, setGroupName ] = useState('')

  const [ ingredientValue, setIngredientValue ] = useState({
    name: '',
    id: null,
    amount: '',
    measurement_unit: ''
  })

  const [ GroupIngredients, setGroupIngredients ] = useState([])
  const [ GroupText, setGroupText ] = useState('')
  const [ GroupTime, setGroupTime ] = useState(0)
  const [ GroupFile, setGroupFile ] = useState(null)
  const [
    GroupFileWasManuallyChanged,
    setGroupFileWasManuallyChanged
  ] = useState(false)

  const [ ingredients, setIngredients ] = useState([])
  const [ showIngredients, setShowIngredients ] = useState(false)
  const [ loading, setLoading ] = useState(true)
  const history = useHistory()

  useEffect(_ => {
    if (ingredientValue.name === '') {
      return setIngredients([])
    }
    api
      .getIngredients({ name: ingredientValue.name })
      .then(ingredients => {
        setIngredients(ingredients)
      })
  }, [ingredientValue.name])

  useEffect(_ => {
    api.getTags()
      .then(tags => {
        setValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])

  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getGroup ({
      Group_id: id
    }).then(res => {
      const {
        image,
        tags,
        cooking_time,
        name,
        ingredients,
        text
      } = res
      setGroupText(text)
      setGroupName(name)
      setGroupTime(cooking_time)
      setGroupFile(image)
      setGroupIngredients(ingredients)


      const tagsValueUpdated = value.map(item => {
        item.value = Boolean(tags.find(tag => tag.id === item.id))
        return item
      })
      setValue(tagsValueUpdated)
      setLoading(false)
    })
    .catch(err => {
      history.push('/Groups')
    })
  }, [value])

  const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
    setIngredientValue({
      ...ingredientValue,
      id,
      name,
      measurement_unit
    })
  }

  const checkIfDisabled = () => {
    return GroupText === '' ||
    GroupName === '' ||
    GroupIngredients.length === 0 ||
    value.filter(item => item.value).length === 0 ||
    GroupTime === '' ||
    GroupFile === '' ||
    GroupFile === null
  }

  return <Main>
    <Container>
      <MetaTags>
        <title>Редактирование рецепта</title>
        <meta name="description" content="Продуктовый помощник - Редактирование рецепта" />
        <meta property="og:title" content="Редактирование рецепта" />
      </MetaTags>
      <Title title='Редактирование рецепта' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          const data = {
            text: GroupText,
            name: GroupName,
            ingredients: GroupIngredients.map(item => ({
              id: item.id,
              amount: item.amount
            })),
            tags: value.filter(item => item.value).map(item => item.id),
            cooking_time: GroupTime,
            image: GroupFile,
            Group_id: id
          }
          api
            .updateGroup(data, GroupFileWasManuallyChanged)
            .then(res => {
              history.push(`/Groups/${id}`)
            })
            .catch(err => {
              const { non_field_errors, ingredients, cooking_time } = err
              console.log({  ingredients })
              if (non_field_errors) {
                return alert(non_field_errors.join(', '))
              }
              if (ingredients) {
                return alert(`Ингредиенты: ${ingredients.filter(item => Object.keys(item).length).map(item => {
                  const error = item[Object.keys(item)[0]]
                  return error && error.join(' ,')
                })[0]}`)
              }
              if (cooking_time) {
                return alert(`Время готовки: ${cooking_time[0]}`)
              }
              const errors = Object.values(err)
              if (errors) {
                alert(errors.join(', '))
              }
            })
        }}
      >
        <Input
          label='Название рецепта'
          onChange={e => {
            const value = e.target.value
            setGroupName(value)
          }}
          value={GroupName}
        />
        <CheckboxGroup
          label='Теги'
          values={value}
          className={styles.checkboxGroup}
          labelClassName={styles.checkboxGroupLabel}
          tagsClassName={styles.checkboxGroupTags}
          checkboxClassName={styles.checkboxGroupItem}
          handleChange={handleChange}
        />
        <div className={styles.ingredients}>
          <div className={styles.ingredientsInputs}>
            <Input
              label='Ингредиенты'
              className={styles.ingredientsNameInput}
              inputClassName={styles.ingredientsInput}
              labelClassName={styles.ingredientsLabel}
              onChange={e => {
                const value = e.target.value
                setIngredientValue({
                  ...ingredientValue,
                  name: value
                })
              }}
              onFocus={_ => {
                setShowIngredients(true)
              }}
              value={ingredientValue.name}
            />
            <div className={styles.ingredientsAmountInputContainer}>
              <Input
                className={styles.ingredientsAmountInput}
                inputClassName={styles.ingredientsAmountValue}
                onChange={e => {
                  const value = e.target.value
                  setIngredientValue({
                    ...ingredientValue,
                    amount: value
                  })
                }}
                value={ingredientValue.amount}
              />
              {ingredientValue.measurement_unit !== '' && <div className={styles.measurementUnit}>{ingredientValue.measurement_unit}</div>}
            </div>
            {showIngredients && ingredients.length > 0 && <IngredientsSearch
              ingredients={ingredients}
              onClick={({ id, name, measurement_unit }) => {
                handleIngredientAutofill({ id, name, measurement_unit })
                setIngredients([])
                setShowIngredients(false)
              }}
            />}
          </div>
          <div className={styles.ingredientsAdded}>
            {GroupIngredients.map(item => {
              return <div
                className={styles.ingredientsAddedItem}
              >
                <span className={styles.ingredientsAddedItemTitle}>{item.name}</span> <span>-</span> <span>{item.amount}{item.measurement_unit}</span> <span
                  className={styles.ingredientsAddedItemRemove}
                  onClick={_ => {
                    const GroupIngredientsUpdated = GroupIngredients.filter(ingredient => {
                      return ingredient.id !== item.id
                    })
                    setGroupIngredients(GroupIngredientsUpdated)
                  }}
                >Удалить</span>
              </div>
            })}
          </div>
          <div
            className={styles.ingredientAdd}
            onClick={_ => {
              if (ingredientValue.amount === '' || ingredientValue.name === '') { return }
              setGroupIngredients([...GroupIngredients, ingredientValue])
              setIngredientValue({
                name: '',
                id: null,
                amount: '',
                measurement_unit: ''
              })
            }}
          >
            Добавить ингредиент
          </div>
        </div>
        <div className={styles.cookingTime}>
          <Input
            label='Время приготовления'
            className={styles.ingredientsTimeInput}
            labelClassName={styles.cookingTimeLabel}
            inputClassName={styles.ingredientsTimeValue}
            onChange={e => {
              const value = e.target.value
              setGroupTime(value)
            }}
            value={GroupTime}
          />
          <div className={styles.cookingTimeUnit}>мин.</div>
        </div>
        <Textarea
          label='Описание рецепта'
          onChange={e => {
            const value = e.target.value
            setGroupText(value)
          }}
          value={GroupText}
        />
        <FileInput
          onChange={file => {
            setGroupFileWasManuallyChanged(true)
            setGroupFile(file)
          }}
          className={styles.fileInput}
          label='Загрузить фото'
          file={GroupFile}
        />
        <div className={styles.actions}>
          <Button
            modifier='style_dark-blue'
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Редактировать рецепт
          </Button>
          <div
            className={styles.deleteGroup}
            onClick={_ => {
              api.deleteGroup({ Group_id: id })
                .then(res => {
                  onItemDelete && onItemDelete()
                  history.push('/Groups')
                })
            }}
          >
            Удалить
          </div>
        </div>
      </Form>
    </Container>
  </Main>
}

export default GroupEdit
