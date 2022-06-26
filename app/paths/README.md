# Основные идеи 

##  Пусть есть дерево
                                               None
                                                |
                                            CATEGORY1
                                        /               \
                              CATEGORY2                CATEGORY3
                            /           \             /         \
                    CATEGORY4         OFFER1   CATEGORY5      CATEGORY6
                        |                        /      \   
                      OFFER2                  CATEGORY7   OFFER3

# 1. import
# Добавление нового элемента:
    Изменяем даты предков до корня    

# Обновление эл-та:
    1. type == 'OFFER' и изменение любое кроме родителя                   2. type == 'OFFER' и изменение родителя                                   
    пусть изменилось offer2 -> offer2*                                    пусть изменилось offer2 -> offer2*                       
                                                                                                                                                     
                                None                                                                  None                         
                                |                                                                     |                            
                            CATEGORY1*                                                            CATEGORY1*                       
                        /               \                                                     /               \                        
              CATEGORY2*                CATEGORY3                                   CATEGORY2*                CATEGORY3*                        
            /           \             /         \                                 /           \             /         \                        
    CATEGORY4*         OFFER1   CATEGORY5      CATEGORY6                  CATEGORY4*         OFFER1   CATEGORY5*      CATEGORY6                         
        |                        /      \                                                                /        \                            
      OFFER2*                  CATEGORY7   OFFER3                                                      CATEGORY7*   OFFER3                        
                                                                                                              |                         
                                                                                                            OFFER2*                         
    -> обновить время у преков до корня.                               -> обновить время у новых и старых предков до корня.  

    

    3. type == 'CATEGORY' и изменение любое кроме родителя                   4. type == 'CATEGORY' и изменение родителя                                   
    пусть изменилось CATEGORY4 -> CATEGORY4*                                    пусть изменилось CATEGORY4 -> CATEGORY4*                       
                                                                                                                                                    
                            None                                                                  None                         
                            |                                                                     |                            
                        CATEGORY1*                                                            CATEGORY1*                       
                    /               \                                                     /               \                        
          CATEGORY2*                CATEGORY3                                   CATEGORY2*                CATEGORY3*                        
        /           \             /         \                                            \             /         \                        
    CATEGORY4*         OFFER1   CATEGORY5      CATEGORY6                                OFFER1   CATEGORY5*      CATEGORY6                         
    |                        /      \                                                                  /        \                            
    OFFER2                  CATEGORY7   OFFER3                                                        CATEGORY7*   OFFER3                        
                                                                                                          \                         
                                                                                                           CATEGORY4*   
                                                                                                                  |      
                                                                                                                OFFER2 
    -> обновить время у преков до корня.                               -> обновить время у новых и старых предков до корня.  

    Итог: Если обновление затронули parentId   -> нужно обновить время у старого родителя до корня и нового родиеля до корня
          Если parentId не изменился -> обновляем время предков до корея 

# 2. delete
    1. type == 'OFFER'                                               2. type == 'CATEGORY' и изменение родителя                                   
    пусть удаляем offer2                                                    пусть удаляем CATEGORY2                        
                                                                                                                                                     
                                None                                                                  None                         
                                |                                                                     |                            
                            CATEGORY1*                                                            CATEGORY1*                       
                        /               \                                                                      \                        
              CATEGORY2*                CATEGORY3                                                           CATEGORY3*                        
            /           \             /         \                                                          /         \                        
    CATEGORY4*         OFFER1   CATEGORY5      CATEGORY6                                             CATEGORY5*      CATEGORY6                         
                                /      \                                                                /        \                            
                               CATEGORY7   OFFER3                                                      CATEGORY7*   OFFER3                        
                                                                                                                                       
                                                                                                                                        
    -> удалить offer2 и удалить ссылку у родителя                              -> удалить CATEGORY2 + детей!! и удалить ссылку у родителя  .  

     Итог: Если удаление offer -> удаление себя и факт у родителя
           Если CATEGORY -> рекурсивно вниз удаляем +себя+факт у родителя