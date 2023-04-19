# Importing packages
import streamlit as st 
import cv2
from PIL import Image
import numpy as np 
import tensorflow as tf
from annotated_text import annotated_text
import webbrowser

# Remove deprecation warnings
st.set_option('deprecation.showfileUploaderEncoding', False)

# Function to laod the image file
@st.cache_data
def load_image(image_file):
	pet_image = Image.open(image_file)
	return pet_image		

# Function to precess image to the correct size
def process_image(_pet_image):
	new_img = np.array(_pet_image.convert('RGB'))
	img = cv2.cvtColor(new_img,1)	        

	# Resizing the image
	img_array = cv2.resize(img, (IMG_SIZE, IMG_SIZE))	
	data = np.array(img_array).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
	return data

# Function to load the model
def load_petModel():
	model = tf.keras.models.load_model('./FreezeModel_tf06')    
	return model

# function to predict the pet breed
@st.cache_data
def predict_breed(_model, data):
	# predict the pet breed using the data
	image_pred = _model.predict(data)

	# convert values in the array from one-hot encoding to decimal numbers
	image_pred_id = [ np.argmax(i)+1 for i in image_pred]

	# Get the pet breed from the data 
	pet_breed = classes[image_pred_id[0]-1].title()
	return pet_breed


# Start of Program

# Get all classes of the breed
classes = [
	'Abyssinian','American bulldog', 'American pit bull_terrier', 'Basset hound',
	'Beagle','Bengal','Birman','Bombay','Boxer','British shorthair','Chihuahua',
	'Egyptian mau','English cocker spaniel','English setter','German shorthaired',
	'Great pyrenees','Havanese','Japanese chin','Keeshond','Leonberger','Maine coon',
	'Miniature pinscher','Newfoundland','Persian','Pomeranian','Pug','Ragdoll',
	'Russian blue','Saint bernard','Samoyed','Scottish terrier','Shiba inu','Siamese',
	'Sphynx','Staffordshire bull terrier','Wheaten terrier','Yorkshire terrier'
] 
# Setting image pixel side size
IMG_SIZE = 299

# Assigning Image to variable
cat_dog = './images/cat-dog.jpg'
st.title("Pet Breed Detection for Online Store")
st.markdown("""---""")

activities = ["Detection","Search Store","About"]
choice = st.sidebar.selectbox("Select Activty",activities)

if choice == 'Detection':
	# Detection type
	detection_choice = st.radio(
	"How do you want to detect your Pet's Breed?",
	("AI Detection", "Manual Detection"))
	if detection_choice == "AI Detection":

		st.subheader("AI Dog and Cat Breed Detection")

		image_file = st.file_uploader("Upload your Pet's Image",type=['jpg','png','jpeg'])

		if image_file is not None:
			# Calling the load_image function
			pet_image = load_image(image_file)		
			st.text("Original Image")			
			st.image(pet_image,width=400)
			# Delete a single key-value pair
			st.session_state["pet_breedname"] = ""
			st.session_state["image_file"] = image_file	
			

		if st.button("Process"):		
			if image_file is not None:
				# Calling the process_image function	
				data = process_image(pet_image)
				with st.spinner('Please Wait while AI Fetches the Pet Breed...'):
					# Calling the load_model function
					reloaded_model = load_petModel()

				# Calling the predict_breed function to predict the pet breed using the data
				st.balloons()
				pet_breed = predict_breed(reloaded_model, data)		
				st.session_state["pet_breedname"] = pet_breed
				#st.session_state["image_file"] = image_file	
				st.markdown("""---""")
				# Display results
				annotated_text(
				("The breed of the pet is ", "#6ff"),
				(pet_breed, "fcc"),
				)				
			else:
				st.error("Please upload a valid image of your pet")
	if detection_choice == "Manual Detection":
		
		if "pet_breedname" not in st.session_state:
			st.session_state["pet_breedname"] = ""

		image_file = cat_dog
		st.image(image_file,width=400)
		st.session_state["image_file"] = image_file

		pet_breedname = st.selectbox("Select your Pet's Breed Here!", classes)
		#my_input = st.text_input("Select your Pet's Breed Here!", st.session_state["my_input"])
		submit = st.button("Process")
		if submit:
			st.session_state["pet_breedname"] = pet_breedname
			
			# Display results
			annotated_text(
			("You have Selected: ", "#6ff"),
			(pet_breedname, "fcc"),
			)       
	
		
elif choice == 'Search Store':

	# Initialization null for 'pet_breedname' and 'image_file' if they are empty
	if "pet_breedname" not in st.session_state:
		st.session_state["pet_breedname"] = ""

	if "image_file" not in st.session_state:
		st.session_state["image_file"] = ""

	st.subheader("Welcome to the Pet Store")	
	if st.session_state["pet_breedname"] == "":
		st.error("Process your Pet's Breed in the 'Detection' Page to Access the Store")
	else:
		st.markdown("Search for your Pet's Products Here!")		
		image_file= st.session_state["image_file"]
		st.success(f'The name of the Pet breed is {st.session_state["pet_breedname"]}')
		# Calling the load_image function
		pet_image = load_image(image_file)				
		st.image(pet_image,width=400)	
		st.markdown("""---""")
		store_type = ["Apparel","Accessory","Food", "Pet Toy", "Veterinary", "All Products"]
		store_choice = st.selectbox("What do you want to get for your pet?", store_type)	
		pet_breed = st.session_state["pet_breedname"]	
		if store_choice == "Apparel":
			st.subheader(f"Get Apparels for your {pet_breed} pet")
			if st.button("Access Store"):
				webbrowser.open(f'https://www.google.com/search?q=Apparels+for+my+{pet_breed}+pet')
		elif store_choice == "Accessory":
			st.subheader(f"Get Accessories for your {pet_breed} pet")
			if st.button("Access Store"):
				webbrowser.open(f'https://www.google.com/search?q=Accessories+for+my+{pet_breed}+pet')
		elif store_choice == "Food":
			st.subheader(f"Get Food Items for your {pet_breed} pet")
			if st.button("Access Store"):
				webbrowser.open(f'https://www.google.com/search?q=Food+items+for+my+{pet_breed}+pet')
		elif store_choice == "Pet Toy":
			st.subheader(f"Get Toys for your {pet_breed} pet")
			if st.button("Access Store"):
				webbrowser.open(f'https://www.google.com/search?q=Toys+for+my+{pet_breed}+pet')
		elif store_choice == "Veterinary":
			st.subheader(f"Get Veterinary Care for your {pet_breed} pet")
			if st.button("Access Store"):
				webbrowser.open(f'https://www.google.com/search?q=Veterinary+Care+for+my+{pet_breed}+pet')
		elif store_choice == "All Products":
			st.subheader(f"Get Various Products for your {pet_breed} pet")
			if st.button("Access Store"):
				webbrowser.open(f'https://www.google.com/search?q=Various+Products+for+my+{pet_breed}+pet')

elif choice == 'About':	
	
	st.subheader("About Pet Breed Detection App")
	st.markdown("""---""")

	st.image(cat_dog, width=400)

	st.markdown("Built with Streamlit by Okeoma O. Ihunwo")
	st.markdown("Student No.: 229154449")
	st.markdown("Course: MSc Applied Data Science")
	st.markdown("School of Computer Science")	
	st.text("University of Sunderland (2022/3 - Sunderland - ASUND")
	st.markdown("""---""")	
	st.success("ONLINE STORE FOR PETS USING MACHINE LEARNING TO DETECT PET BREEDS")


st.markdown("""---""")
st.text("Built with Streamlit and OpenCV")
