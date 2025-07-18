// # Create a Rate Limiting Rule Class/Function that will take in a rule which will be evaluated against incoming messages.
 
// # The rule must contain:
// # 1. The threshold (maximum number of matching messages allowed by a person)
// # 2. The evaluation time window in seconds (the time window over which counts are tracked) 
 
 
// # The class should support the below operation:

// # should_throttle(message, current_time int) bool ->  Which will take in a message, a monotonically increasing timestamp (seconds)
// # and return true if it breaches the rule threshold for the current time window, or false otherwise.
 
// # Example:
 
// # If we have the below rule:

// # rule = RateLimitingRule(1, 10)
 
// # And the following messages:
// # message1 = {"name" : "John"}
// # message2 = {"name" : "Josh"}
// # message3 = {"name" : "John"}
// # message4 = {"name" : "Josh"}
// # message5 = {"name" : "John"}
// # message6 = {"name" : "Josh"}
 
// # Calling should_throttle with the below arguments should result in result3 being true 
// # result1 = rule.should_throttle(message1, 5) # should return false
// # result2 = rule.should_throttle(message2, 6) # should return false
// # result3 = rule.should_throttle(message3, 9) # should return true because this is the second occurrence within the time window
// # result4 = rule.should_throttle(message4, 11) # should return true 
// # result5 = rule.should_throttle(message5, 16) # should return false since the message is now outside of the time window
// # result6 = rule.should_throttle(message6, 16) # should return true because this is the second occurrence within the time window
// 20   1   20-1 19 >threshold=10

// 20  
package main
import "fmt"
type RuleLimit struct{
  MessageThreshold int
  EvalTime int
//userReQuestMap
  }
  
  //20 
  
  func (ruleLimit RuleLimit)should_throttle(message User, current_time int) bool{
   // userReQuestMap[userName][len(userReQuestMap[userName])-1]//15
      currentRequestTime:=current_time  //20
     // currentRequestTime-userReQuestMap[userName][len(userReQuestMap[userName])-1]>timeWindow  5>10
      userName:=message.Name
      var returnResult bool
  if(!userReQuestMap[userName]||(currentRequestTime-userReQuestMap[userName][len(userReQuestMap[userName])-1]>ruleLimit.EvalTime && len(userReQuestMap[userName])<=ruleLimit.MessageThreshold)){
    //allow it
    //add to the list
    //syncMAP LOadOrStore and GET
    userReQuestMap[userName]=append(userReQuestMap[userName],currentRequestTime)
    
  }else{
         returnResult= true;
  }
  
  //Current Time 55
  //evaluation time window  is 10
  //2,4,5[_________]
  
 // because 55-10=44
 //
 
 20=currentTIme
 EvalTime=10
  josh =[1,2,15]  1 is gone  ,
  for userName,requestGatheredTimes:=range userReQuestMap{
  var allowedRequest []int
    for timeIdx:=0;timeIdx<len(requestGatheredTimes);timeIdx++ {
        if(requestGatheredTimes[timeIdx]<(currentRequestTime-ruleLimit.EvalTime) ){//len(userReQuestMap[userName])<=ruleLimit.MessageThreshold)
        //dont take these/
    
      }else{
        allowedRequest=append(allowedRequest,requestGatheredTimes[timeIdx])
      }
    
    }//
    userReQuestMap[userName]=allowedRequest
  
  }
    
    return returnResult
  }
  
  type User struct{
    Name string
  }
  
  var userReQuestMap map[string][]int
func main(){
	// fmt.Printf("Hello")
  
  // user["john"]=[5]
  // ["josh"]=[6]
  ruleLimit:=RuleLimit{
     MessageThreshold : 1,
    EvalTime :10,
    
  }
  userReQuestMap=make(map[string][]int)//requestTime  user vs his allowedRequestTImes
  
  
  message1 := User{Name: "John"}
 message2 :=User{Name:  "Josh"}
 message3 := User{Name:  "John"}
 message4 := User{Name:  "Josh"}
message5 :=User{Name:  "John"}
message6 :=User{Name:  "Josh"}



 
// Calling should_throttle with the below arguments should result in result3 being true 
 result1 = ruleLimit.should_throttle(message1, 5)// # should return false
 fmt.Println(result1)
 result2 = ruleLimit.should_throttle(message2, 6) //# should return false
 fmt.Println(result2)
 
 result3 = ruleLimit.should_throttle(message3, 9) //# should return true because this is the second occurrence within the time window
 fmt.Println(result3)
 
//  result4 = ruleLimit.should_throttle(message4, 11) //# should return true 
//  result5 = ruleLimit.should_throttle(message5, 16) //# should return false since the message is now outside of the time window
//  result6 = ruleLimit.should_throttle(message6, 16) //# should return true because this is the second occurrence within the time window
  
  
  

  
  
  
  
}

