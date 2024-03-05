import { Container, FileInput, Input, Title, CheckboxGroup, Main, Form, Button, Checkbox, Textarea } from '../../components'
import styles from './styles.module.css'
import api from '../../api'
import { useEffect, useState } from 'react'
import { useTags } from '../../utils'
import { useParams, useHistory } from 'react-router-dom'
import MetaTags from 'react-meta-tags'

const RecipeEdit = ({ onItemDelete }) => {
  const { value, handleChange, setValue } = useTags()
  const [ recipeName, setRecipeName ] = useState('')
  const [ grTitle, setGrTitle ] = useState('')
  const [ recipeText, setRecipeText ] = useState('')
  const [ recipeTime, setRecipeTime ] = useState(0)
  const [ recipeFile, setRecipeFile ] = useState(null)
  const [
    recipeFileWasManuallyChanged,
    setRecipeFileWasManuallyChanged
  ] = useState(false)
  const [date, setDate ] = useState(new Date())

  //const [ ingredients, setIngredients ] = useState([])
  //const [ showIngredients, setShowIngredients ] = useState(false)
  const [ loading, setLoading ] = useState(true)
  const history = useHistory()

 // useEffect(_ => {
 //   if (ingredientValue.name === '') {
 //     return setIngredients([])
 //   }
 //   api
 //     .getSchedule({ group: id })
 //     .then(schedule => {
 //       setIngredients(schedule)
 //     })
 // }, [ingredientValue.name])

  useEffect(_ => {
    api.getTags()
      .then(tags => {
        setValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])

  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getRecipe ({
      recipe_id: id
    }).then(res => {
      const {
        image,
        rubric,
        number_of_lessons,
        name,
        description,
        title,
        begin_at
      } = res
      setRecipeText(description)
      setRecipeName(name)
      setRecipeTime(number_of_lessons)
      setRecipeFile(image)
      setGrTitle(title)
      setDate(begin_at)

      //setRecipeIngredients(schedule)


      const tagsValueUpdated = value.map(item => {
        item.value = Boolean(rubric.find(tag => tag.id === item.id))
        return item
      })
      setValue(tagsValueUpdated)
      setLoading(false)
    })
    .catch(err => {
      history.push('/groups')
    })
  }, [value])

  //const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
  //  setIngredientValue({
   //   ...ingredientValue,
   //   id,
   //   name,
    //  measurement_unit
  //  })
 // }

  const checkIfDisabled = () => {
    return recipeText === '' ||
    recipeName === '' ||
    //recipeIngredients.length === 0 ||
    value.filter(item => item.value).length === 0 ||
    recipeTime === '' ||
    recipeFile === '' ||
    recipeFile === null
  }

  return <Main>
    <Container>
      <MetaTags>
        <title>Редактирование группы</title>
        <meta name="description" content="Продуктовый помощник - Редактирование рецепта" />
        <meta property="og:title" content="Редактирование рецепта" />
      </MetaTags>
      <Title title='Редактирование группы' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          const data = {
            text: recipeText,
            name: recipeName,
            //ingredients: recipeIngredients.map(item => ({
            //  id: item.id,
             // amount: item.amount
           // })),
            rubric: value.filter(item => item.value).map(item => item.id),
            number_of_lessons: recipeTime,
            image: recipeFile,
            recipe_id: id,
            begin_at: date

          }
          api
            .updateRecipe(data, recipeFileWasManuallyChanged)
            .then(res => {
              history.push(`/groups/${id}`)
            })
            .catch(err => {
              const { non_field_errors, number_of_lessons } = err
              if (non_field_errors) {
                return alert(non_field_errors.join(', '))
              }
             // if (ingredients) {
             //   return alert(`Ингредиенты: ${ingredients.filter(item => Object.keys(item).length).map(item => {
             //     const error = item[Object.keys(item)[0]]
             //     return error && error.join(' ,')
              //  })[0]}`)
             // }
              if (number_of_lessons) {
                return alert(`Количество часов: ${number_of_lessons[0]}`)
              }
              const errors = Object.values(err)
              if (errors) {
                alert(errors.join(', '))
              }
            })
        }}
      >
        <Input
          label='Название группы'
          onChange={e => {
            const value = e.target.value
            setRecipeName(value)
          }}
          value={recipeName}
        />
        <CheckboxGroup
          label='Рубрики'
          values={value}
          className={styles.checkboxGroup}
          labelClassName={styles.checkboxGroupLabel}
          tagsClassName={styles.checkboxGroupTags}
          checkboxClassName={styles.checkboxGroupItem}
          handleChange={handleChange}
        />

        <div className={styles.cookingTime}>
          <Input
            label='Количество занятий'
            className={styles.ingredientsTimeInput}
            labelClassName={styles.cookingTimeLabel}
            inputClassName={styles.ingredientsTimeValue}
            onChange={e => {
              const value = e.target.value
              setRecipeTime(value)
            }}
            value={recipeTime}
          />
          <div className={styles.cookingTimeUnit}>ч.</div>
        </div>
        <Textarea
          label='Описание группы'
          onChange={e => {
            const value = e.target.value
            setRecipeText(value)
          }}
          value={recipeText}
        />
        <FileInput
          onChange={file => {
            setRecipeFileWasManuallyChanged(true)
            setRecipeFile(file)
          }}
          className={styles.fileInput}
          label='Загрузить фото'
          file={recipeFile}
        />
        <Input
            label="Дата начала"
            onChange={(e) => {
              const value = e.target.value;
              setDate(value);
            }}
            value={date}
        />
        <div className={styles.actions}>
          <Button
            modifier='style_dark-blue'
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Сохранить
          </Button>
          <div
            className={styles.deleteRecipe}
            onClick={_ => {
              api.deleteRecipe({ recipe_id: id })
                .then(res => {
                  onItemDelete && onItemDelete()
                  history.push('/groups')
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

export default RecipeEdit
