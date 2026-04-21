(module
  (type (;0;) (func (param i32) (result i32)))
  (type (;1;) (func))
  (type (;2;) (func (param i32)))
  (type (;3;) (func (result i32)))
  (func (;0;) (type 1)
    nop)
  (func (;1;) (type 2) (param i32)
    local.get 0
    global.set 0)
  (func (;2;) (type 0) (param i32) (result i32)
    global.get 0
    local.get 0
    i32.sub
    i32.const -16
    i32.and
    local.tee 0
    global.set 0
    local.get 0)
  (func (;3;) (type 3) (result i32)
    global.get 0)
  (func (;4;) (type 0) (param i32) (result i32)
    (local i32)
    i32.const 1124
    i32.load
    local.set 1
    local.get 0
    i32.load8_s
    call 5
    local.set 0
    block  ;; label = @1
      block (result i32)  ;; label = @2
        local.get 1
        i32.const 3
        i32.le_s
        if  ;; label = @3
          i32.const 1091
          local.get 1
          i32.const 1073
          i32.add
          i32.load8_u
          local.get 0
          i32.const 255
          i32.and
          i32.eq
          br_if 1 (;@2;)
          drop
          br 2 (;@1;)
        end
        local.get 0
        i32.const -32
        i32.add
        i32.const 255
        i32.and
        i32.const 94
        i32.gt_u
        br_if 1 (;@1;)
        i32.const 1091
        local.get 1
        i32.const 47
        i32.ne
        br_if 0 (;@2;)
        drop
        i32.const 1104
        i32.const 1078
        local.get 0
        i32.const 125
        i32.eq
        select
      end
      return
    end
    i32.const 1121
    i32.const 42
    i32.store8
    i32.const 1124
    i32.const 0
    i32.store
    i32.const 1078)
  (func (;5;) (type 0) (param i32) (result i32)
    (local i32)
    i32.const 1124
    i32.const 1124
    i32.load
    i32.const 1
    i32.add
    i32.const 49
    i32.rem_u
    local.tee 1
    i32.store
    i32.const 1121
    i32.const 1121
    i32.load8_u
    local.get 1
    i32.const 1024
    i32.add
    i32.load8_u
    local.get 0
    i32.xor
    i32.xor
    local.tee 0
    i32.store8
    local.get 0
    i32.const 24
    i32.shl
    i32.const 24
    i32.shr_s)
  (memory (;0;) 256 256)
  (global (;0;) (mut i32) (i32.const 5244176))
  (export "memory" (memory 0))
  (export "review" (func 4))
  (export "_start" (func 0))
  (export "stackSave" (func 3))
  (export "stackAlloc" (func 2))
  (export "stackRestore" (func 1))
  (data (;0;) (i32.const 1024) "*9g~q-!!rCA:\09\0c\04\05RB@\19\0awQB\05#6[\0cgf\22\00K'8Grn[u+,2^SGZ\22ptm{\00what's this?\00zzz...\00\00\00\00\00\00\00thx ...zzzzzz...\00*")
  (data (;1;) (i32.const 1136) "\10\05P"))
