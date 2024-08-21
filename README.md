# Pynar_Code_Fixer_Chatbot
## [TR]
Projemiz, kodlamaya yeni başlayan veya bu alanda kendini geliştirmek isteyen kullanıcıların hata ayıklama sürecini daha verimli hale getirmeyi amaçlamaktadır. Kodlama, her yaştan bireyin dahil olabileceği bir hobi haline gelmiştir ve bu durum, tüm yaş gruplarına hitap eden, basit bir arayüzle kullanılabilen ve başlangıç seviyesindeki geliştiricilere kolaylık sağlayan araçlara olan ihtiyacı artırmıştır.

Bu doğrultuda, projemiz özellikle başlangıç seviyesindeki geliştiriciler için tasarlanmış olan Pynar Python editörü ile entegre edilecek şekilde geliştirilmiştir. Amacımız, Pynar IDE'si içerisinde kod yazarken bir hata meydana geldiğinde, bu hatayı otomatik olarak düzelten ve kullanıcının isteğine bağlı olarak hatalı kodun yerine düzeltilmiş kodu koyan bir çözüm sunmaktır. Ayrıca, hataların nedenlerini açıklayarak kullanıcının hatalarından öğrenmesini ve kendini geliştirmesini sağlamayı hedefliyoruz.

## [EN]
Our project is designed to streamline the debugging process for users who are new to programming or those looking to enhance their coding skills. As coding increasingly becomes a hobby accessible to individuals of all ages, the need for tools that cater to diverse user groups with simple interfaces and ease of use has emerged. Recognizing this, our project is specifically aimed at integrating with the Pynar Python editor, a platform tailored for beginner developers.

The goal of our project is to provide a seamless experience within the Pynar IDE, where, upon encountering an error in the code, the tool automatically offers corrected code suggestions and allows the user to replace the erroneous code with the improved version. Additionally, the tool will provide detailed explanations of the errors to help users understand and learn from their mistakes, ultimately aiding in their development as proficient programmers.

## How does it work?
We decided to run the model on colab servers to avoid the situation where users do not have enough graphics card power to run the model. The user will send the error code from his local machine to the colab server via anvil and the server will run the model input and return the result back to the user via anvil. The model used is small and has low generalization capability in Turkish, but high generalization capability for Python. Since English is the language in which it succeeds, the results were obtained in English. Then, using google translate, the results were translated into Turkish and sent to the user.

## Flowchart
- This flowchart expresses the logic of the end-to-end system.
![chatbot](https://github.com/user-attachments/assets/33f3a39a-f49b-4978-8d7d-4c5990a8a703)

## Requirements
- Python 3.8 or higher is required.
- We used anvil tool for communication between Colab servers and local machine. Moreover you need anvil api key to run the models. (https://anvil.works/)
- Install the necessary libraries:
```
pip3 install -r requirements.txt
```
