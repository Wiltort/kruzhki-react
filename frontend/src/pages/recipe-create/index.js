import {
  Container,
  IngredientsSearch,
  FileInput,
  Input,
  Title,
  CheckboxGroup,
  Main,
  Form,
  Button,
  Checkbox,
  Textarea,
} from "../../components";
import styles from "./styles.module.css";
import api from "../../api";
import { useEffect, useState } from "react";
import { useTags } from "../../utils";
import { useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";
//import DatePicker from 'react-date-picker';


const RecipeCreate = ({ onEdit }) => {
  const { value, handleChange, setValue } = useTags();
  const [recipeName, setRecipeName] = useState("");
  const [grTitle, setGrTitle] = useState("");
  const history = useHistory();
  //const [ ingredientValue, setIngredientValue ] = useState({
  //  name: '',
  //  id: null,
  //  amount: '',
  //  measurement_unit: ''
  //})
  //const [ recipeIngredients, setRecipeIngredients ] = useState([])
  const [recipeText, setRecipeText] = useState("");
  const [recipeTime, setRecipeTime] = useState("");
  const [recipeFile, setRecipeFile] = useState(null);
  const [date, setDate] = useState(new Date());

  //const [ ingredients, setIngredients ] = useState([])
  //const [ showIngredients, setShowIngredients ] = useState(false)
  //useEffect(_ => {
  //  if (ingredientValue.name === '') {
  //    return setIngredients([])
  //  }
  //  api
  //    .getIngredients({ name: ingredientValue.name })
  //    .then(ingredients => {
  //      setIngredients(ingredients)
  //    })
  //}, [ingredientValue.name])

  useEffect((_) => {
    api.getTags().then((tags) => {
      setValue(tags.map((tag) => ({ ...tag, value: true })));
    });
  }, []);

  //const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
  //  setIngredientValue({
  //    ...ingredientValue,
  //    id,
  //    name,
  //    measurement_unit
  //  })
  //}
 
  const checkIfDisabled = () => {
    return (
      recipeText === "" ||
      recipeName === "" ||
      //recipeIngredients.length === 0 ||
      //value.filter(item => item.value).length === 0 ||
      recipeTime === "" ||
      recipeFile === "" ||
      recipeFile === null
    );
  };

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Создание группы</title>
          <meta
            name="description"
            content="Продуктовый помощник - Создание рецепта"
          />
          <meta property="og:title" content="Создание рецепта" />
        </MetaTags>
        <Title title="Создание группы" />
        <Form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            const data = {
              description: recipeText,
              name: recipeName,
              title: grTitle,
              //ingredients: recipeIngredients.map(item => ({
              //  id: item.id,
              //  amount: item.amount
              //})),
              rubric: value.filter((item) => item.value).map((item) => item.id),
              number_of_lessons: recipeTime,
              image: recipeFile,
              begin_at: date,
            };
            api
              .createRecipe(data)
              .then((res) => {
                history.push(`/groups/${res.id}`);
              })
              .catch((err) => {
                const { non_field_errors, number_of_lessons } = err;
                if (non_field_errors) {
                  return alert(non_field_errors.join(", "));
                }

                if (number_of_lessons) {
                  return alert(`Количество часов: ${number_of_lessons[0]}`);
                }
                const errors = Object.values(err);
                if (errors) {
                  alert(errors.join(", "));
                }
              });
          }}
        >
          <Input
            label="Код группы"
            onChange={(e) => {
              const value = e.target.value;
              setRecipeName(value);
            }}
          />
          <Input
            label="Название группы"
            onChange={(e) => {
              const value = e.target.value;
              setGrTitle(value);
            }}
          />

          <CheckboxGroup
            label="Рубрика"
            values={value}
            className={styles.checkboxGroup}
            labelClassName={styles.checkboxGroupLabel}
            tagsClassName={styles.checkboxGroupTags}
            checkboxClassName={styles.checkboxGroupItem}
            handleChange={handleChange}
          />

          <div className={styles.cookingTime}>
            <Input
              label="Количество занятий"
              className={styles.ingredientsTimeInput}
              labelClassName={styles.cookingTimeLabel}
              inputClassName={styles.ingredientsTimeValue}
              onChange={(e) => {
                const value = e.target.value;
                setRecipeTime(value);
              }}
              value={recipeTime}
            />
            <div className={styles.cookingTimeUnit}>ч.</div>
          </div>
          <Textarea
            label="Описание группы"
            onChange={(e) => {
              const value = e.target.value;
              setRecipeText(value);
            }}
          />
          <FileInput
            onChange={(file) => {
              setRecipeFile(file);
            }}
            className={styles.fileInput}
            label="Загрузить фото"
          />
          <Input
            label="Дата начала"
            onChange={(e) => {
              const value = e.target.value;
              setDate(value);
            }}
          />
          <Button
            modifier="style_dark-blue"
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Создать группу
          </Button>
        </Form>
      </Container>
    </Main>
  );
};

export default RecipeCreate;
